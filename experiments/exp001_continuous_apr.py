"""
Experiment 001

Continuous APR instead of quartile APR.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import CONFIG


def continuous_apr(df: pd.DataFrame) -> pd.Series:
    """
    Maps risk score (f11) continuously to APR.

    Lowest risk  -> 18%
    Highest risk -> 29%
    """

    risk = df["f11"]

    risk_min = risk.min()
    risk_max = risk.max()

    apr = CONFIG.apr_low + (
        (risk - risk_min)
        / (risk_max - risk_min + 1e-9)
    ) * (
        CONFIG.apr_high - CONFIG.apr_low
    )

    return apr


def create_economics_continuous(df: pd.DataFrame):

    apr = continuous_apr(df)

    df["interest_revenue"] = (
        df["f1"]
        * apr
        * (1 - df["f11"])
    )

    return df