"""
Conditional Premium Score
"""

from __future__ import annotations

import pandas as pd

from src.config import CONFIG
from src.premium_engagement import premium_engagement_score


def rank(series: pd.Series) -> pd.Series:

    return series.rank(
        pct=True,
        method="average",
    )


def conditional_premium_score(
    df: pd.DataFrame,
) -> pd.Series:

    premium = premium_engagement_score(df)

    spend = rank(
        df["category_spend"]
    )

    # ---------------------------------
    # Soft Gate
    # ---------------------------------

    threshold = CONFIG.conditional_spend_threshold

    gate = (
        spend
        .sub(threshold)
        .clip(lower=0)
        / (1 - threshold)
    )

    return premium * gate