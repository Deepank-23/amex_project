"""
Economics Layer
Creates revenue and cost features.
"""

from __future__ import annotations

import pandas as pd


from src.config import CONFIG

APR_MAP = {
    0: CONFIG.apr_low,
    1: CONFIG.apr_mid1,
    2: CONFIG.apr_mid2,
    3: CONFIG.apr_high,
}


def create_economics(df: pd.DataFrame) -> pd.DataFrame:

    # -----------------------------------------
    # APR
    # -----------------------------------------

    risk_q = pd.qcut(
        df["f11"],
        4,
        labels=False,
        duplicates="drop",
    )

    df["apr"] = risk_q.map(APR_MAP)

    # -----------------------------------------
    # Spend
    # -----------------------------------------

    df["f7_clipped"] = df["f7"].clip(lower=0)

    df["category_spend"] = (

        df["f6"]

        + df["f7_clipped"]

        + df["f8"]

        + df["f9"]

        + df["f10"]

    )

    # -----------------------------------------
    # Revenue
    # -----------------------------------------

    df["interest_revenue"] = (

        df["f1"]

        * df["apr"]

        * (1 - df["f11"])

    )

    df["interchange_revenue"] = (

        df["category_spend"]

        * CONFIG.interchange_rate

    )

    df["rewards_breakage"] = (

        (df["f4"] - df["f21"])

        .clip(lower=0)

        * 0.01

        * CONFIG.breakage_value

    )

    # -----------------------------------------
    # Costs
    # -----------------------------------------

    df["expected_credit_loss"] = (

        df["f1"]

        * df["f11"]

        * 0.5

    )

    df["benefit_cost"] = (

        df["f13"] * 50

        + df["f14"]

        + df["f15"] * 15

        + df["f16"]

    )

    df["servicing_cost"] = (

        (df["f2"] + df["f3"])

        * 25

    )

    # -----------------------------------------
    # Net Profit
    # -----------------------------------------

    df["NetProfit"] = (

        df["interest_revenue"]

        + df["interchange_revenue"]

        + df["rewards_breakage"]

        - df["expected_credit_loss"]

        - df["benefit_cost"]

        - df["servicing_cost"]

    )

    return df