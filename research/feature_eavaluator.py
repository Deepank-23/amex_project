"""
Feature Evaluator

Evaluates how well a feature identifies valuable customers.
"""

from __future__ import annotations

import pandas as pd

TOP_PERCENT = 0.20


def evaluate_feature(
    df: pd.DataFrame,
    feature: str,
) -> None:

    top_n = int(len(df) * TOP_PERCENT)

    ranked = df.sort_values(feature, ascending=False)

    top = ranked.head(top_n)
    bottom = ranked.tail(top_n)

    print("\n" + "=" * 80)
    print(f"Feature: {feature}")
    print("=" * 80)

    metrics = [
        "f1",
        "f5",
        "f11",
        "interest_revenue",
        "interchange_revenue",
        "NetProfit",
        "LTV_Profitability",
    ]

    results = []

    for metric in metrics:

        top_mean = top[metric].mean()
        bottom_mean = bottom[metric].mean()

        if abs(bottom_mean) < 1e-9:
            ratio = float("inf")
        else:
            ratio = top_mean / bottom_mean

        results.append({
            "Metric": metric,
            "Top20": top_mean,
            "Bottom20": bottom_mean,
            "Ratio": ratio,
        })

    result_df = pd.DataFrame(results)

    print(result_df.round(3).to_string(index=False))