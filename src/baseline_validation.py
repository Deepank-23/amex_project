"""
Baseline Validation
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_raw_scores(
    current_path: str,
    historical_path: str,
):

    print("\n")
    print("=" * 80)
    print("BASELINE VALIDATION")
    print("=" * 80)

    current = pd.read_csv(current_path)

    if historical_path.endswith(".xlsx"):
        historical = pd.read_excel(historical_path)
    else:
        historical = pd.read_csv(historical_path)

    print("\nRows")

    print(f"Current    : {len(current)}")
    print(f"Historical : {len(historical)}")

    merged = current.merge(
        historical,
        on="ID",
        suffixes=("_current", "_historical"),
    )

    print(f"Merged     : {len(merged)}")

    # -------------------------------------------------------
    # Correlations
    # -------------------------------------------------------

    pearson = merged["Prediction_current"].corr(
        merged["Prediction_historical"],
        method="pearson",
    )

    spearman = merged["Prediction_current"].corr(
        merged["Prediction_historical"],
        method="spearman",
    )

    print("\n")
    print("=" * 80)
    print("CORRELATION")
    print("=" * 80)

    print(f"Pearson  : {pearson:.8f}")
    print(f"Spearman : {spearman:.8f}")

    # -------------------------------------------------------
    # Error
    # -------------------------------------------------------

    merged["Difference"] = (
        merged["Prediction_current"]
        - merged["Prediction_historical"]
    )

    merged["AbsoluteDifference"] = (
        merged["Difference"].abs()
    )

    print("\n")
    print("=" * 80)
    print("ERROR")
    print("=" * 80)

    print(
        "Mean Absolute Error :",
        merged["AbsoluteDifference"].mean(),
    )

    print(
        "Median Absolute Error :",
        merged["AbsoluteDifference"].median(),
    )

    print(
        "Maximum Difference :",
        merged["AbsoluteDifference"].max(),
    )

    # -------------------------------------------------------
    # Largest errors
    # -------------------------------------------------------

    report = merged.sort_values(
        "AbsoluteDifference",
        ascending=False,
    )

    output = Path("outputs/reports")

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        output / "baseline_difference_report.csv",
        index=False,
    )

    print("\nSaved report:")
    print(output / "baseline_difference_report.csv")

    return report