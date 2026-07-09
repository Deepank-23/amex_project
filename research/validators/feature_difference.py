"""
Feature Difference Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import CONFIG
from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_feature_shift(
    better_model: str,
    weaker_model: str,
    top_n: int = 50000,
):

    # -----------------------------
    # Load original dataset
    # -----------------------------

    data = pd.read_csv(CONFIG.train_path)

    if "id" in data.columns:
        data = data.rename(columns={"id": "ID"})

    # -----------------------------
    # Load submissions
    # -----------------------------

    submissions = load_submissions()

    better = submissions[better_model].copy()

    better["Rank_Better"] = (
        better["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    weaker = submissions[weaker_model].copy()

    weaker["Rank_Weaker"] = (
        weaker["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    merged = (
        data
        .merge(
            better[["ID", "Rank_Better"]],
            on="ID",
        )
        .merge(
            weaker[["ID", "Rank_Weaker"]],
            on="ID",
        )
    )

    # -----------------------------
    # Rank improvement
    # -----------------------------

    merged["RankGain"] = (
        merged["Rank_Weaker"]
        - merged["Rank_Better"]
    )

    promoted = merged.nlargest(
        top_n,
        "RankGain",
    )

    demoted = merged.nsmallest(
        top_n,
        "RankGain",
    )

    numeric = data.select_dtypes(
        include="number"
    ).columns

    report = []

    for col in numeric:

        if col == "ID":
            continue

        p = promoted[col].mean()
        d = demoted[col].mean()

        if abs(d) > 1e-9:
            percent = 100 * (p - d) / abs(d)
        else:
            percent = 0.0
        report.append(
            {
                "Feature": col,
                "Promoted": p,
                "Demoted": d,
                "Difference": p - d,
                "PercentDifference": percent,
            }
        )

    report = pd.DataFrame(report)

    report["AbsDifference"] = (
        report["Difference"].abs()
    )

    report = report.sort_values(
        "AbsDifference",
        ascending=False,
    )

    report.to_csv(
        REPORT_DIR /
        f"{better_model}_vs_{weaker_model}_feature_diff.csv",
        index=False,
    )

    print()

    print("=" * 80)
    print("TOP FEATURE DIFFERENCES")
    print("=" * 80)

    print(report.head(25))
    print()

    print("Largest Positive Shifts")

    print(report.head(10))

    print()

    print("Largest Negative Shifts")

    print(
        report.sort_values(
            "Difference"
        ).head(10)
    )

    return {
        "top_positive": report.head(10),
        "top_negative": report.sort_values(
            "Difference"
        ).head(10),
        "report": report,
    }


if __name__ == "__main__":

    print("Testing Feature Difference")

    analyze_feature_shift(
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
    )