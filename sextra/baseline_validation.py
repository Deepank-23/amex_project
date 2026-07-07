"""
Baseline Validation
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_against_baseline(
    generated_path: str,
    baseline_path: str,
):

    baseline_file = Path(baseline_path)

    if not baseline_file.exists():

        if baseline_file.suffix.lower() == ".csv":
            xlsx_fallback = baseline_file.with_suffix(".xlsx")

            if xlsx_fallback.exists():
                baseline_file = xlsx_fallback
            else:
                print("=" * 80)
                print("BASELINE VALIDATION")
                print("=" * 80)
                print(f"Baseline file not found: {baseline_path}")
                print("Skipping baseline comparison.")
                return None
        else:

            print("=" * 80)
            print("BASELINE VALIDATION")
            print("=" * 80)
            print(f"Baseline file not found: {baseline_path}")
            print("Skipping baseline comparison.")
            return None

    generated = pd.read_csv(generated_path)

    if baseline_file.suffix.lower() in {".xlsx", ".xls"}:
        baseline = pd.read_excel(baseline_file)
    else:
        baseline = pd.read_csv(baseline_file)

    print("=" * 80)
    print("BASELINE VALIDATION")
    print("=" * 80)

    # -------------------------
    # Basic checks
    # -------------------------

    print(f"Generated Rows : {len(generated)}")
    print(f"Baseline Rows  : {len(baseline)}")

    assert len(generated) == len(baseline)

    # -------------------------
    # Merge
    # -------------------------

    merged = generated.merge(
        baseline,
        on="ID",
        suffixes=("_new", "_old"),
    )

    # -------------------------
    # Correlation
    # -------------------------

    corr = merged["Prediction_new"].corr(
        merged["Prediction_old"],
        method="spearman",
    )

    print(f"\nSpearman Rank Correlation : {corr:.6f}")

    # -------------------------
    # Mean Difference
    # -------------------------

    diff = (
        merged["Prediction_new"]
        - merged["Prediction_old"]
    ).abs()

    print(f"Mean Rank Difference : {diff.mean():.2f}")

    print(f"Maximum Difference   : {diff.max()}")

    # -------------------------
    # Top 20 overlap
    # -------------------------

    top_new = set(
        merged.nsmallest(
            100000,
            "Prediction_new",
        )["ID"]
    )

    top_old = set(
        merged.nsmallest(
            100000,
            "Prediction_old",
        )["ID"]
    )

    overlap = len(
        top_new.intersection(top_old)
    ) / 100000

    print(
        f"\nTop20 Overlap : {overlap:.4%}"
    )

    return merged