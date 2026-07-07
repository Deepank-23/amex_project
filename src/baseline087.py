"""
BEST 0.87 Baseline Model
"""

from __future__ import annotations
from src.config import CONFIG
import pandas as pd


def z(series: pd.Series) -> pd.Series:

    std = series.std()

    if std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - series.mean()) / std


def create_best087_score(
    df: pd.DataFrame,
) -> pd.DataFrame:

    # -----------------------------------------
    # Z-score Components
    # -----------------------------------------

    z_interest = z(
        df["interest_revenue"]
    )

    z_interchange = z(
        df["interchange_revenue"]
    )

    z_breakage = z(
        df["rewards_breakage"]
    )

    # -----------------------------------------
    # Interaction
    # -----------------------------------------

    interaction = (

        df["f1"].rank(pct=True)

        *

        df["category_spend"].rank(pct=True)

    )

    z_interaction = z(
        interaction
    )

    # -----------------------------------------
    # Risk Discount
    # -----------------------------------------

    z_risk = z(
        -df["f11"]
    )

    # -----------------------------------------
    # Final BEST Score
    # -----------------------------------------

    df["BEST_Score"] = (

        CONFIG.interest_weight * z_interest

        +

        CONFIG.merchant_weight * z_interchange

        +

        CONFIG.breakage_weight * z_breakage

        +

        CONFIG.interaction_weight * z_interaction

        +

        CONFIG.risk_weight * z_risk

    )

    return df