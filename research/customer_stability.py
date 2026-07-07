"""
Customer Stability Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def customer_stability():

    submissions = load_submissions()

    merged = None

    for name, df in submissions.items():

        temp = df.rename(
            columns={
                "Prediction": name
            }
        )

        if merged is None:
            merged = temp
        else:
            merged = merged.merge(
                temp,
                on="ID",
            )

    score_columns = [
        c for c in merged.columns
        if c != "ID"
    ]

    merged["MeanRank"] = merged[score_columns].mean(axis=1)
    merged["StdRank"] = merged[score_columns].std(axis=1)
    merged["MinRank"] = merged[score_columns].min(axis=1)
    merged["MaxRank"] = merged[score_columns].max(axis=1)

    merged["Range"] = (
        merged["MaxRank"]
        - merged["MinRank"]
    )

    merged = merged.sort_values(
        "StdRank",
        ascending=False,
    )

    merged.to_csv(
        REPORT_DIR / "customer_stability.csv",
        index=False,
    )

    print("\nTop unstable customers\n")

    print(
        merged[
            [
                "ID",
                "StdRank",
                "Range",
            ]
        ].head(20)
    )

    return merged


if __name__ == "__main__":

    customer_stability()