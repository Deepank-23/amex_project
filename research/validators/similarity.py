"""
Experiment Similarity Validation
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def compare_similarity(
    baseline_name: str,
    experiment_name: str,
) -> dict:
    """
    Compare one experiment against one baseline submission.
    """

    submissions = load_submissions()

    missing = [
        name for name in (baseline_name, experiment_name)
        if name not in submissions
    ]

    if missing:
        available = ", ".join(sorted(submissions))
        raise KeyError(
            f"Missing submission(s): {', '.join(missing)}. "
            f"Available submissions: {available}"
        )

    baseline = submissions[baseline_name]
    experiment = submissions[experiment_name]

    merged = baseline.merge(
        experiment,
        on="ID",
        suffixes=("_baseline", "_experiment"),
    )

    # -------------------------------------------------
    # Correlations
    # -------------------------------------------------

    pearson = merged["Prediction_baseline"].corr(
        merged["Prediction_experiment"],
        method="pearson",
    )

    spearman = merged["Prediction_baseline"].corr(
        merged["Prediction_experiment"],
        method="spearman",
    )

    # -------------------------------------------------
    # Absolute Errors
    # -------------------------------------------------

    difference = (
        merged["Prediction_baseline"]
        - merged["Prediction_experiment"]
    )

    mae = difference.abs().mean()

    median = difference.abs().median()

    maximum = difference.abs().max()

    # -------------------------------------------------
    # Top 20% Overlap
    # -------------------------------------------------

    k = int(len(merged) * 0.20)

    baseline_top = set(
        merged.nsmallest(
            k,
            "Prediction_baseline",
        )["ID"]
    )

    experiment_top = set(
        merged.nsmallest(
            k,
            "Prediction_experiment",
        )["ID"]
    )

    overlap = len(
        baseline_top & experiment_top
    ) / k

    # -------------------------------------------------
    # Save detailed report
    # -------------------------------------------------

    report = merged.copy()

    report["Difference"] = difference

    report["AbsoluteDifference"] = (
        difference.abs()
    )

    report = report.sort_values(
        "AbsoluteDifference",
        ascending=False,
    )

    report.to_csv(
        REPORT_DIR /
        f"{baseline_name}_vs_{experiment_name}_similarity.csv",
        index=False,
    )

    # -------------------------------------------------
    # Print Summary
    # -------------------------------------------------

    print(f"Baseline   : {baseline_name}")
    print(f"Experiment : {experiment_name}")

    print()

    print(f"Pearson           : {pearson:.6f}")
    print(f"Spearman          : {spearman:.6f}")
    print(f"Top20 Overlap     : {overlap:.4f}")

    print()

    print(f"MAE               : {mae:.6f}")
    print(f"Median AE         : {median:.6f}")
    print(f"Maximum Difference: {maximum:.6f}")

    return {
        "pearson": pearson,
        "spearman": spearman,
        "top20_overlap": overlap,
        "mae": mae,
        "median": median,
        "maximum": maximum,
    }


if __name__ == "__main__":

    compare_similarity(
        "AMEX_R1_BEST_087",
        "BEST_BASELINE",
    )