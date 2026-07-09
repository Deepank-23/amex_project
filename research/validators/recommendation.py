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


def _report_from(value: pd.DataFrame | dict) -> pd.DataFrame:

    if isinstance(value, pd.DataFrame):
        return value

    report = value.get("report")

    if isinstance(report, pd.DataFrame):
        return report

    raise TypeError(
        "business must be a DataFrame report or a dict containing a DataFrame under 'report'"
    )


def generate_recommendation(
    similarity: dict,
    movement: pd.DataFrame,
    business: pd.DataFrame | dict,
    features: pd.DataFrame,
):

    print()
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)

    spearman = similarity["spearman"]

    business_report = _report_from(business)

    spend = _value(business_report, "f5")

    revolve = _value(business_report, "f1")

    risk = _value(business_report, "f11")

    net_profit = _value(business_report, "NetProfit")

    ltv = _value(business_report, "LTV_Profitability")

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