"""
Validation Module
"""

from __future__ import annotations

import pandas as pd


def describe(name, series):

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(series.describe())

    print()


def validate_components(df: pd.DataFrame):

    describe(
        "Interest Revenue",
        df["interest_revenue"],
    )

    describe(
        "Interchange Revenue",
        df["interchange_revenue"],
    )

    describe(
        "Rewards Breakage",
        df["rewards_breakage"],
    )

    describe(
        "Net Profit",
        df["NetProfit"],
    )

    describe(
        "LTV Profitability",
        df["LTV_Profitability"],
    )

    describe(
        "Score V2",
        df["Score_v2"],
    )

    describe(
        "BEST Score",
        df["BEST_Score"],
    )