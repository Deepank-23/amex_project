"""
BEST 0.87 Baseline Model
"""

from __future__ import annotations

from collections.abc import Sequence

from src.config import CONFIG
import pandas as pd
from src.customer_value import relationship_score
from src.interactions import rank_product
from src.premium_engagement import premium_engagement_score
from src.conditional_premium import (
    conditional_premium_score,
)

from src.benefit_cost import (
    benefit_intensity,
)
def z(series: pd.Series) -> pd.Series:

    std = series.std()

    if std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - series.mean()) / std


def create_best087_score(
    df: pd.DataFrame,
) -> pd.DataFrame:

    premium_weight = CONFIG.premium_weight
    premium_weights: Sequence[float] | None = None

    if isinstance(premium_weight, Sequence) and not isinstance(
        premium_weight,
        (str, bytes),
    ):
        premium_weights = premium_weight
        premium_weight = 1.0

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
    benefit_efficiency = (
        df["benefit_cost"]
        /
        (
            df["interest_revenue"]
            + df["interchange_revenue"]
        ).clip(lower=1)
    )

    z_benefit = z(
        -benefit_efficiency
    )

    # -----------------------------------------
    # Relationship
    # -----------------------------------------

    z_relationship = z(
        relationship_score(df)
    )
    z_conditional = z(
        conditional_premium_score(df)
    )

    z_premium = z(
        premium_engagement_score(
            df,
            weights=premium_weights,
        )
    )

    # -----------------------------------------
    # Final BEST Score
    # -----------------------------------------

    score = (

        0.374 * z_interest

        +

        0.501 * z_interchange

        +

        0.085 * z_breakage

        +

        0.14 * z_interaction

        +

        0.15 * z_risk

        +

        0.15 * z_benefit

    )

    if CONFIG.use_relationship_score:
        score += (
            CONFIG.relationship_weight
            * z_relationship
        )
    if CONFIG.use_premium_score:

        score += (

            premium_weight

            * z_premium

        )

    if CONFIG.use_conditional_premium:

        score += (

            CONFIG.conditional_premium_weight
            * z_conditional

        )

    df["BEST_Score"] = score

    return df