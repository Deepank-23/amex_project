"""
Customer Difference Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from research.submission_loader import load_submissions

REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def analyze_customer_movement(
    model1: str,
    model2: str,
):

    submissions = load_submissions()

    df1 = submissions[model1].copy()
    df2 = submissions[model2].copy()

    # Convert prediction to actual ranking
    df1["Baseline_Rank"] = (
        df1["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df2["Experiment_Rank"] = (
        df2["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    merged = df1[["ID", "Baseline_Rank"]].merge(
        df2[["ID", "Experiment_Rank"]],
        on="ID",
    )

    merged["Rank_Change"] = (
        merged["Baseline_Rank"]
        - merged["Experiment_Rank"]
    )

    merged["Absolute_Change"] = (
        merged["Rank_Change"].abs()
    )

    top20 = int(len(merged) * 0.20)

    merged["Baseline_Top20"] = (
        merged["Baseline_Rank"] <= top20
    )

    merged["Experiment_Top20"] = (
        merged["Experiment_Rank"] <= top20
    )

    merged["Entered_Top20"] = (
        (~merged["Baseline_Top20"])
        &
        (merged["Experiment_Top20"])
    )

    merged["Exited_Top20"] = (
        (merged["Baseline_Top20"])
        &
        (~merged["Experiment_Top20"])
    )

    merged = merged.sort_values(
        "Absolute_Change",
        ascending=False,
    )

    output = (
        REPORT_DIR /
        f"{model1}_vs_{model2}_customer_changes.csv"
    )

    merged.to_csv(
        output,
        index=False,
    )

    print("=" * 80)
    print("CUSTOMER MOVEMENT")
    print("=" * 80)

    print()

    print(
        "Average Rank Change:",
        merged["Absolute_Change"].mean()
    )

    print(
        "Median Rank Change:",
        merged["Absolute_Change"].median()
    )

    print()

    print(
        "Entered Top20:",
        merged["Entered_Top20"].sum()
    )

    print(
        "Exited Top20:",
        merged["Exited_Top20"].sum()
    )

    print()

    print("Largest Promotions")

    print(
        merged.sort_values(
            "Rank_Change",
            ascending=False,
        ).head(20)
    )

    print()

    print("Largest Demotions")

    print(
        merged.sort_values(
            "Rank_Change",
            ascending=True,
        ).head(20)
    )

    return merged