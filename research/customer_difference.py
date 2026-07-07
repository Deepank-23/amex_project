"""
Customer Difference Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.submission_loader import load_submissions

REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def compare_customers(
    model1: str,
    model2: str,
):

    submissions = load_submissions()

    df1 = submissions[model1].rename(
        columns={"Prediction": "Rank_1"}
    )

    df2 = submissions[model2].rename(
        columns={"Prediction": "Rank_2"}
    )

    merged = df1.merge(
        df2,
        on="ID",
    )

    merged["Rank_Difference"] = (
        merged["Rank_1"] - merged["Rank_2"]
    )

    merged["Absolute_Difference"] = (
        merged["Rank_Difference"].abs()
    )

    merged = merged.sort_values(
        "Absolute_Difference",
        ascending=False,
    )

    output = (
        REPORT_DIR /
        f"{model1}_vs_{model2}.csv"
    )

    merged.to_csv(
        output,
        index=False,
    )

    print("=" * 80)
    print(model1)
    print("vs")
    print(model2)
    print("=" * 80)

    print()

    print("Largest Rank Changes")

    print(
        merged.head(20)
    )

    return merged


if __name__ == "__main__":

    compare_customers(
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
    )