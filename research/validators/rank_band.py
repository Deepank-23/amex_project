"""
Rank Band Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_rank_bands(
    baseline_name: str,
    experiment_name: str,
):

    submissions = load_submissions()

    baseline = submissions[baseline_name].copy()
    experiment = submissions[experiment_name].copy()

    baseline["BaselineRank"] = (
        baseline["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    experiment["ExperimentRank"] = (
        experiment["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    merged = baseline.merge(
        experiment,
        on="ID",
        suffixes=("_baseline", "_experiment"),
    )

    merged["RankShift"] = (
        merged["BaselineRank"]
        - merged["ExperimentRank"]
    )

    bands = [
        (1, 1000),
        (1001, 10000),
        (10001, 50000),
        (50001, 80000),
        (80001, 120000),
        (120001, 200000),
        (200001, merged["BaselineRank"].max()),
    ]

    report = []

    for low, high in bands:

        band = merged[
            merged["BaselineRank"].between(low, high)
        ]

        promoted = (band["RankShift"] > 0).sum()

        demoted = (band["RankShift"] < 0).sum()

        report.append(
            {
                "RankBand": f"{low:,}-{high:,}",
                "Customers": len(band),
                "MeanShift": band["RankShift"].mean(),
                "MedianShift": band["RankShift"].median(),
                "AbsShift": band["RankShift"].abs().mean(),
                "Promoted": promoted,
                "Demoted": demoted,
                "LargestPromotion": band["RankShift"].max(),
                "LargestDemotion": band["RankShift"].min(),
            }
        )

    report = pd.DataFrame(report)

    report.to_csv(
        REPORT_DIR /
        f"{baseline_name}_vs_{experiment_name}_rank_bands.csv",
        index=False,
    )

    print()
    print("=" * 100)
    print("RANK BAND ANALYSIS")
    print("=" * 100)

    print(report)

    return report