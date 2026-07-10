"""
Ranking
"""

from __future__ import annotations

import pandas as pd


def create_rank(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df["Prediction"] = (

        df["BEST_Score"]

        .rank(

            ascending=False,

            method="dense",

        )

    )

    return df