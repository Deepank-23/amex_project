"""
Experiment Runner
"""

from pathlib import Path
import subprocess

EXPERIMENTS = {
    "baseline": "main.py",
}


def run_experiment(name: str):

    if name not in EXPERIMENTS:
        raise ValueError(f"Unknown experiment: {name}")

    print("=" * 80)
    print(f"RUNNING {name.upper()}")
    print("=" * 80)

    subprocess.run(
        ["python", EXPERIMENTS[name]],
        check=True,
    )

    print("\nExperiment Complete")


if __name__ == "__main__":

    run_experiment("baseline")