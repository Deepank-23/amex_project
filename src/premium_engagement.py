"""
Premium Engagement Score
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from src.config import CONFIG


def rank(series: pd.Series) -> pd.Series:
    return series.rank(
        pct=True,
        method="average",
    )


def premium_engagement_score(
    df: pd.DataFrame,
    weights: Sequence[float] | None = None,
) -> pd.Series:

    if weights is None:
        lounge_weight = CONFIG.lounge_weight
        airline_weight = CONFIG.airline_weight
        cab_weight = CONFIG.cab_weight
        entertainment_weight = CONFIG.entertainment_weight
        email_open_weight = CONFIG.email_open_weight
        email_click_weight = CONFIG.email_click_weight
    else:
        (
            lounge_weight,
            airline_weight,
            cab_weight,
            entertainment_weight,
            email_open_weight,
            email_click_weight,
        ) = weights

    score = (

        rank(df["f13"])

        * lounge_weight

        +

        rank(df["f14"])

        * airline_weight

        +

        rank(df["f15"])

        * cab_weight

        +

        rank(df["f16"])

        * entertainment_weight

        +

        rank(df["f22"])

        * email_open_weight

        +

        rank(df["f23"])

        * email_click_weight

    )

    return score