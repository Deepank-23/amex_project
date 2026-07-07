"""
Lifetime Value Layer
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def z(series: pd.Series) -> pd.Series:

    std = series.std()

    if std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - series.mean()) / std


def create_ltv(df: pd.DataFrame) -> pd.DataFrame:

    BASE_YEARS = 4.0

    # -----------------------------------------
    # Benefit Count
    # -----------------------------------------

    df["benefit_count"] = (

        (df["f13"] > 0).astype(int)

        + (df["f14"] > 0).astype(int)

        + (df["f15"] > 0).astype(int)

        + (df["f16"] > 0).astype(int)

    )

    # -----------------------------------------
    # Engagement
    # -----------------------------------------

    df["engagement_z"] = (

        z(df["f12"])

        + z(df["f22"])

        + z(df["f19"])

        + z(df["f20"])

    ) / 4

    # -----------------------------------------
    # Distress
    # -----------------------------------------

    df["distress_penalty"] = (

        z(df["f2"]) * 0.5

        + z(df["f3"]) * 1.0

        + z(df["f11"]) * 0.5

    )

    # -----------------------------------------
    # Benefit Bonus
    # -----------------------------------------

    benefit_bonus = np.select(

        [

            df["benefit_count"] >= 3,

            df["benefit_count"] == 2,

            df["benefit_count"] == 1,

            df["benefit_count"] == 0,

        ],

        [

            0.35,

            0.15,

            0.05,

            -0.05,

        ],

    )

    # -----------------------------------------
    # Retention
    # -----------------------------------------

    raw = (

        1

        + benefit_bonus

        + 0.10 * df["engagement_z"]

        - 0.15 * df["distress_penalty"]

    )

    df["RetentionMultiplier"] = raw.clip(lower=0.4,upper=2.0)

    # -----------------------------------------
    # LTV
    # -----------------------------------------

    df["LTV_Years"] = (

        BASE_YEARS

        * df["RetentionMultiplier"]

    )

    df["LTV_Profitability"] = (

        df["NetProfit"]

        * df["LTV_Years"]

    )

    return df