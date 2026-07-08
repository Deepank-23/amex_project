from __future__ import annotations

import numpy as np
import pandas as pd

from src.constants import (
    APR_MAP,
    INTERCHANGE_RATE,
    BREAKAGE_VALUE,
)
from src.interactions import rank_product

def category_spend(df: pd.DataFrame) -> pd.Series:

    return (
        df["f6"]
        + df["f7"].clip(lower=0)
        + df["f8"]
        + df["f9"]
        + df["f10"]
    )

def reward_breakage(df: pd.DataFrame) -> pd.Series:

    return (
        df["f4"] - df["f21"]
    ).clip(lower=0)

def risk_quartile(df: pd.DataFrame) -> pd.Series:

    return pd.qcut(
        df["f11"],
        4,
        labels=False,
        duplicates="drop",
    )

def apr(df: pd.DataFrame) -> pd.Series:

    quartile = risk_quartile(df)

    return quartile.map(APR_MAP).astype(float)

def interest_revenue(df: pd.DataFrame) -> pd.Series:

    return (
        df["f1"]
        * apr(df)
        * (1 - df["f11"])
    )

def merchant_revenue(df: pd.DataFrame) -> pd.Series:

    return (
        category_spend(df)
        * INTERCHANGE_RATE
    )

def reward_value(df: pd.DataFrame) -> pd.Series:

    return (
        reward_breakage(df)
        * BREAKAGE_VALUE
    )

def interaction(df: pd.DataFrame) -> pd.Series:

    return rank_product(
        df["f1"],
        category_spend(df),
    )

def risk_discount(df: pd.DataFrame) -> pd.Series:

    return -df["f11"]

def build_components(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build all issuer economics components.

    Returns
    -------
    DataFrame
        Contains every component used by the ranking model.
    """

    comp = pd.DataFrame(index=df.index)

    comp["interest"] = interest_revenue(df)

    comp["merchant"] = merchant_revenue(df)

    comp["breakage"] = reward_value(df)

    comp["interaction"] = interaction(df)

    comp["risk"] = risk_discount(df)

    return comp