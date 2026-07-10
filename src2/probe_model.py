"""
Research Probe Models
"""

from __future__ import annotations

import pandas as pd


class ProbeModel:

    def __init__(self):

        self.name = "BASE"

    def predict(
        self,
        df: pd.DataFrame,
    ) -> pd.Series:

        raise NotImplementedError