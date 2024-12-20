from .simulator import Simulation
from .info_parser import get_positions
from .read_non_blocking import NonBlockingBytesReader

from subprocess import Popen, PIPE
import sys
import os
import time
import datetime

import argparse

from jelka_validator import DataReader

parser = argparse.ArgumentParser(description="Run Jelka FMF simulation.")

parser.add_argument("runner", type=str, nargs="?", help="How to run your program.")
parser.add_argument("target", type=str, help="Your program name.")
parser.add_argument(
    "--positions", type=str, help="File with LED positions. Leave empty for automatic detection or random.", required=False
)


def main(header_wait: float = 0.5):
    print(
        f"[SIMULATION] You are executing JelkaSim from '{os.getcwd()}' using Python '{sys.executable}'.",
        file=sys.stderr,
        flush=True,
    )

    args = parser.parse_args()

    cmd = []
    if args.runner:
        if not args.target:
            # TODO: UI
            raise ValueError("[SIMULATION] You must provide a target program.")
    if args.target:
        if args.runner:
            cmd = [args.runner, args.target]
        elif args.target.endswith(".py"):
            cmd = [sys.executable, args.target]
        else:
            cmd = [args.target]
    if not cmd:
        raise ValueError("[SIMULATION] You must provide a target program. Wait for the next update...")

    # Provide default file locations
    filenames = [
        os.path.join(os.getcwd(), "positions.csv"),
        os.path.join(os.path.dirname(args.target), "positions.csv"),
        os.path.join(os.path.dirname(sys.argv[0]), "positions.csv"),
        os.path.join(os.getcwd(), "../../data/positions.csv"),
        os.path.join(os.path.dirname(args.target), "../../data/positions.csv"),
        os.path.join(os.path.dirname(sys.argv[0]), "../../data/positions.csv"),
    ]

    # Allow specifying a custom path
    if args.positions:
        filenames = [args.positions]

    # Resolve relative paths to absolute paths
    filenames = [os.path.abspath(filename) for filename in filenames]

    # Try to load positions from various files
    positions = get_positions(filenames)

    print("[SIMULATION] Initializing the simulation window.", file=sys.stderr, flush=True)
    sim = Simulation(positions)
    sim.init()

    print(f"[SIMULATION] Running {cmd} at {datetime.datetime.now()}.", file=sys.stderr, flush=True)

    with Popen(cmd, stdout=PIPE) as p:
        breader = NonBlockingBytesReader(p.stdout.read1)  # type: ignore
        dr = DataReader(breader.start())  # type: ignore
        dr.update()

        t_start = time.time()
        while time.time() - t_start < header_wait and dr.header is None:
            dr.update()
            time.sleep(0.01)

        if dr.header is None:
            raise ValueError(f"[SIMULATION] No header found in the first {header_wait} seconds. Is your program running?")

        while sim.running:
            c = next(dr)
            dr.user_print()
            sim.set_colors(dict(zip(range(len(c)), c)))
            sim.frame()
        breader.close()
        sim.quit()

    print(
        f"[SIMULATION] Finished running at {datetime.datetime.now()} (took {time.time() - t_start:.2f} seconds).",
        file=sys.stderr,
        flush=True,
    )
