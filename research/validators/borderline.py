"""
Borderline Customer Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_borderline(
    baseline_name: str,
    experiment_name: str,
    lower: int = 80000,
    upper: int = 120000,
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

    border = merged[
        merged["BaselineRank"].between(
            lower,
            upper,
        )
    ].copy()

    entered = border[
        border["ExperimentRank"] < lower
    ]

    exited = border[
        border["ExperimentRank"] > upper
    ]

    report = {
        "Customers": len(border),
        "EnteredTopRegion": len(entered),
        "ExitedTopRegion": len(exited),
        "AverageShift": border["RankShift"].mean(),
        "MedianShift": border["RankShift"].median(),
        "AverageAbsoluteShift": border["RankShift"].abs().mean(),
        "LargestPromotion": border["RankShift"].max(),
        "LargestDemotion": border["RankShift"].min(),
    }

    border.sort_values(
        "RankShift",
        ascending=False,
    ).to_csv(
        REPORT_DIR /
        f"{baseline_name}_vs_{experiment_name}_borderline.csv",
        index=False,
    )

    print()
    print("=" * 100)
    print("BORDERLINE ANALYSIS")
    print("=" * 100)

    for key, value in report.items():
        print(f"{key:25} : {value}")

    return report
