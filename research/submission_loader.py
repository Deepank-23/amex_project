"""
Submission Loader

Loads every historical submission automatically.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd


SUBMISSION_FOLDER = Path(
    "data/previous_submission"
)

CURRENT_SUBMISSION_FOLDER = Path(
    "outputs/raw_scores"
)


def submission_name(file: Path) -> str:
    name = file.stem

    if name.endswith("_SCORE"):
        name = name[:-6]

    return name


def load_submissions(
    names: Iterable[str] | None = None,
):

    submissions = {}
    requested = set(names) if names is not None else None

    files = sorted(
        list(SUBMISSION_FOLDER.glob("*"))
        + list(CURRENT_SUBMISSION_FOLDER.glob("*"))
    )

    for file in files:

        if file.suffix.lower() not in [
            ".csv",
            ".xlsx",
            ".xls",
        ]:
            continue

        name = submission_name(file)

        if requested is not None and name not in requested:
            continue

        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        submissions[name] = df

    return submissions


if __name__ == "__main__":

    submissions = load_submissions()

    print()

    print("=" * 80)

    print("Loaded submissions")

    print("=" * 80)

    for name in submissions:

        print(name)

        print(submissions[name].shape)

        print()
