"""
Benefit Cost Features
"""

from __future__ import annotations

import pandas as pd


def benefit_cost(
    df: pd.DataFrame,
) -> pd.Series:

    return (

        32 * df["f13"]

        + df["f14"]

        + 15 * df["f15"]

        + df["f16"]

    )


def benefit_intensity(
    df: pd.DataFrame,
) -> pd.Series:

    spend = (
        df["category_spend"]
        .clip(lower=1)
    )

    return (

        benefit_cost(df)

        / spend

    )