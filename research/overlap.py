"""
Submission Overlap Analysis
"""

from __future__ import annotations

import pandas as pd


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize submission format.
    """

    cols = {c.lower(): c for c in df.columns}

    id_col = cols.get("id")
    pred_col = cols.get("prediction")

    if id_col is None or pred_col is None:
        raise ValueError(
            "Submission must contain ID and Prediction columns."
        )

    return df.rename(
        columns={
            id_col: "ID",
            pred_col: "Prediction",
        }
    )[["ID", "Prediction"]]


def compare_submissions(
    sub1: pd.DataFrame,
    sub2: pd.DataFrame,
    name1: str = "Submission 1",
    name2: str = "Submission 2",
):

    sub1 = _prepare(sub1)
    sub2 = _prepare(sub2)

    merged = sub1.merge(
        sub2,
        on="ID",
        suffixes=("_1", "_2"),
    )

    print("\n")
    print("=" * 80)
    print(f"{name1}  vs  {name2}")
    print("=" * 80)

    # --------------------------------------------
    # Correlations
    # --------------------------------------------

    pearson = merged["Prediction_1"].corr(
        merged["Prediction_2"],
        method="pearson",
    )

    spearman = merged["Prediction_1"].corr(
        merged["Prediction_2"],
        method="spearman",
    )

    print(f"Pearson  : {pearson:.6f}")
    print(f"Spearman : {spearman:.6f}")

    # --------------------------------------------
    # Top-K overlap
    # --------------------------------------------

    total = len(merged)

    for pct in [0.01, 0.05, 0.10, 0.20]:

        k = int(total * pct)

        top1 = set(
            merged.nsmallest(
                k,
                "Prediction_1",
            )["ID"]
        )

        top2 = set(
            merged.nsmallest(
                k,
                "Prediction_2",
            )["ID"]
        )

        overlap = len(top1 & top2) / k

        print(
            f"Top {int(pct*100):>2}% overlap : {overlap:.4%}"
        )

    # --------------------------------------------
    # Rank Difference
    # --------------------------------------------

    diff = (
        merged["Prediction_1"]
        - merged["Prediction_2"]
    ).abs()

    print()

    print("Mean Rank Difference :", diff.mean())

    print("Median Rank Difference :", diff.median())

    print("Maximum Difference :", diff.max())

    return merged