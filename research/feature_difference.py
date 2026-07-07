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


def feature_difference(
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

    better = submissions[better_model].rename(
        columns={"Prediction": "Rank_Better"}
    )

    weaker = submissions[weaker_model].rename(
        columns={"Prediction": "Rank_Weaker"}
    )

    merged = (
        data
        .merge(better, on="ID")
        .merge(weaker, on="ID")
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

        report.append(
            {
                "Feature": col,
                "Promoted": p,
                "Demoted": d,
                "Difference": p - d,
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

    return report


if __name__ == "__main__":

    feature_difference(
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
    )