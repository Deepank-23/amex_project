"""
Experiment Recommendation
"""

from __future__ import annotations

import pandas as pd


def _value(report: pd.DataFrame, metric: str) -> float:
    row = report.loc[report["Metric"] == metric]

    if row.empty:
        return 0.0

    return float(row["PercentDifference"].iloc[0])


def generate_recommendation(
    similarity: dict,
    movement: pd.DataFrame,
    business: pd.DataFrame,
    features: pd.DataFrame,
):

    print()
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)

    spearman = similarity["spearman"]

    spend = _value(business, "f5")

    revolve = _value(business, "f1")

    risk = _value(business, "f11")

    net_profit = _value(business, "NetProfit")

    ltv = _value(business, "LTV_Profitability")

    print(f"Spearman : {spearman:.4f}")
    print(f"Spend    : {spend:+.2f}%")
    print(f"Revolve  : {revolve:+.2f}%")
    print(f"Risk     : {risk:+.2f}%")
    print(f"Profit   : {net_profit:+.2f}%")
    print(f"LTV      : {ltv:+.2f}%")

    print()

    score = 0

    if spearman >= 0.98:
        score += 1

    if spend > 0:
        score += 1

    if revolve > 0:
        score += 1

    if net_profit > 0:
        score += 1

    if ltv > 0:
        score += 1

    # Lower risk is better
    if risk < 0:
        score += 1

    print(f"Experiment Score : {score}/6")
    print()

    if score >= 5:
        decision = "PASS"

    elif score >= 3:
        decision = "REVIEW"

    else:
        decision = "REJECT"

    print(f"Recommendation : {decision}")

    return decision