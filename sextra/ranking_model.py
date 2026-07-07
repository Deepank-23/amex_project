from __future__ import annotations

import pandas as pd

from src.constants import WEIGHTS

from src.issuer_economics import (
    interest_revenue,
    merchant_revenue,
    reward_value,
    interaction,
    risk_discount,
)
from src.issuer_economics import build_components


def zscore(series: pd.Series) -> pd.Series:
    """
    Standardize a series using z-score.
    """
    std = series.std()

    if std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - series.mean()) / std


class Best087Model:
    def predict(self, df: pd.DataFrame) -> pd.Series:
        comp = build_components(df)

        score = (
            WEIGHTS["interest"] * zscore(comp["interest"]) +
            WEIGHTS["merchant"] * zscore(comp["merchant"]) +
            WEIGHTS["breakage"] * zscore(comp["breakage"]) +
            WEIGHTS["interaction"] * zscore(comp["interaction"]) +
            WEIGHTS["risk"] * zscore(comp["risk"])
        )

        return score