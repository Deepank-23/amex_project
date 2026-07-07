"""
Experiment Tracker
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

import pandas as pd


TRACKER_PATH = Path("research/reports/experiment_tracker.csv")


COLUMNS = [
    "Experiment",
    "Date",
    "Description",
    "Files Changed",
    "Offline Score",
    "Leaderboard",
    "Status",
    "Notes",
]


def initialize_tracker():

    if TRACKER_PATH.exists():
        return

    TRACKER_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(columns=COLUMNS).to_csv(
        TRACKER_PATH,
        index=False,
    )


def log_experiment(
    experiment,
    description,
    files_changed,
    offline_score="",
    leaderboard="",
    status="Pending",
    notes="",
):

    initialize_tracker()

    df = pd.read_csv(TRACKER_PATH)

    new_row = {
        "Experiment": experiment,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Description": description,
        "Files Changed": files_changed,
        "Offline Score": offline_score,
        "Leaderboard": leaderboard,
        "Status": status,
        "Notes": notes,
    }

    df.loc[len(df)] = new_row

    df.to_csv(
        TRACKER_PATH,
        index=False,
    )

    print("\nExperiment Logged\n")

    print(df.tail())


if __name__ == "__main__":

    log_experiment(
        experiment="EXP001",
        description="Continuous APR",
        files_changed="economics.py",
    )