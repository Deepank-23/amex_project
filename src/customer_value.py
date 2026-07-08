"""
Customer Value Components
"""

from __future__ import annotations

import pandas as pd
from src.config import CONFIG

def relationship_score(df: pd.DataFrame) -> pd.Series:
    """
    Measures depth of customer relationship.
    """
    weights = CONFIG.relationship_weights
    relationship = (
        weights["supplementary"]* df["f19"].rank(pct=True) +   # Supplementary Accounts
        weights["charge_cards"] * df["f20"].rank(pct=True) +   # Active Charge Cards
        weights["credit_line"] * df["f17"].rank(pct=True) +   # Credit Line
        weights["consumer_credit"] * df["f18"].rank(pct=True)     # Consumer Credit Line
    )
    assert (
    abs(sum(weights.values()) - 1.0) < 1e-9), "Relationship weights must sum to 1."
    
    return relationship