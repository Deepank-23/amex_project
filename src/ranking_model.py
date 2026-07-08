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
from src.customer_value import relationship_score
from src.config import CONFIG
from src.customer_value import relationship_score

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
        relationship = zscore(
            relationship_score(df)
        )
        comp["relationship"] = relationship_score(df)
        print("\nRelationship Score")
        print(comp["relationship"].describe())
        score = (
            WEIGHTS["interest"] * zscore(comp["interest"]) +
            WEIGHTS["merchant"] * zscore(comp["merchant"]) +
            WEIGHTS["breakage"] * zscore(comp["breakage"]) +
            WEIGHTS["interaction"] * zscore(comp["interaction"]) +
            WEIGHTS["risk"] * zscore(comp["risk"]) +

            WEIGHTS["relationship"] * zscore(comp["relationship"])
        )
        if CONFIG.use_relationship_score:
            score += (
                CONFIG.relationship_weight
                * relationship
            )
        return score