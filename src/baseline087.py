"""
BEST 0.87 Baseline Model
"""

from __future__ import annotations
from src.config import CONFIG
import pandas as pd
from src.customer_value import relationship_score
from src.interactions import rank_product

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


    interaction = rank_product(
        df["f1"],
        df["category_spend"],
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
    # Relationship
    # -----------------------------------------

    z_relationship = z(
        relationship_score(df)
    )

    # -----------------------------------------
    # Final BEST Score
    # -----------------------------------------

    score = (

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

    if CONFIG.use_relationship_score:
        score += (
            CONFIG.relationship_weight
            * z_relationship
        )

    df["BEST_Score"] = score

    return df