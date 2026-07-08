"""
Submission Module
"""

from __future__ import annotations
from src.config import CONFIG
from pathlib import Path

import pandas as pd


def create_submission(
    df: pd.DataFrame,
    score: pd.Series,
    path=CONFIG.submission_path,
) -> pd.DataFrame:

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    submission = pd.DataFrame()

    submission["ID"] = df["ID"]

    # Every customer gets a unique rank
    submission["Prediction"] = (
        score.rank(
            ascending=False,
            method="first",
        ).astype(int)
    )

    submission.to_csv(
        path,
        index=False,
    )

    print(f"\nSubmission saved to:\n{path}")

    return submission

def save_raw_scores(
    df: pd.DataFrame,
    path=CONFIG.raw_score_path,
) -> pd.DataFrame:

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    scores = pd.DataFrame()

    scores["ID"] = df["ID"]

    scores["Prediction"] = df["BEST_Score"]

    scores.to_csv(
        path,
        index=False,
    )

    print(f"\nRaw scores saved to:\n{path}")

    return scores