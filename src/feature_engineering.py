"""
Feature Engineering Module
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.constants import EPSILON

ENGINEERED_FEATURES = {
    "ratio": [],
    "spending": [],
    "credit": [],
    "reward": [],
    "behavior": [],
    "interaction": [],
    "business": []
}

def create_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ratio-based features.
    """

    spend_cols = ["f6", "f7", "f8", "f9", "f10"]

    # Category spend ratios
    for col in spend_cols:

        new_col = f"{col}_ratio"

        df[new_col] = df[col] / (df["f5"] + EPSILON)

        ENGINEERED_FEATURES["ratio"].append(new_col)

    # Revolving balance
    df["revolve_percentage"] = (
        df["f1"] / (df["f5"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "revolve_spend_ratio"
    )

    # Credit utilization
    df["credit_utilization"] = (
        df["f5"] / (df["f17"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "spend_credit_ratio"
    )

    df["spend_utilization"] = (
        df["f1"] / (df["f17"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "revolve_credit_ratio"
    )

    # Consumer credit
    df["spend_consumer_credit_ratio"] = (
        df["f5"] / (df["f18"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "spend_consumer_credit_ratio"
    )

    df["revolve_consumer_credit_ratio"] = (
        df["f1"] / (df["f18"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "revolve_consumer_credit_ratio"
    )

    # Rewards
    df["reward_balance_ratio"] = (
        df["f4"] / (df["f5"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "reward_balance_ratio"
    )

    df["reward_redeem_ratio"] = (
        df["f21"] / (df["f5"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "reward_redeem_ratio"
    )

    df["reward_redemption_efficiency"] = (
        df["f21"] / (df["f4"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "reward_redemption_efficiency"
    )

    # Email engagement
    df["click_open_ratio"] = (
        df["f23"] / (df["f22"] + EPSILON)
    )

    ENGINEERED_FEATURES["ratio"].append(
        "click_open_ratio"
    )

    print(f"Created {len(ENGINEERED_FEATURES['ratio'])} ratio features.")

    return df

def create_spending_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create spending behaviour features.
    """

    spend_cols = ["f6", "f7", "f8", "f9", "f10"]

    # Number of spending categories used
    df["category_count"] = (
        df[spend_cols] > 0
    ).sum(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_count")

    # Mean category spend
    df["category_mean"] = df[spend_cols].mean(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_mean")

    # Maximum category spend
    df["category_max"] = df[spend_cols].max(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_max")

    # Minimum category spend
    df["category_min"] = df[spend_cols].min(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_min")

    # Standard deviation
    df["category_std"] = df[spend_cols].std(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_std")

    # Total category spend
    df["category_total"] = df[spend_cols].sum(axis=1)

    ENGINEERED_FEATURES["spending"].append("category_total")

    # Concentration
    df["category_concentration"] = (
        df["category_max"] /
        (df["category_total"] + EPSILON)
    )

    ENGINEERED_FEATURES["spending"].append(
        "category_concentration"
    )
    df["spending_entropy"] = df.apply(
        spending_entropy,
        axis=1
    )

    ENGINEERED_FEATURES["spending"].append(
        "spending_entropy"
    )   

    print(
        f"Created {len(ENGINEERED_FEATURES['spending'])} spending features."
    )

    return df

def spending_entropy(row):

    spend = row[["f6","f7","f8","f9","f10"]].values

    total = spend.sum()

    if total == 0:
        return 0

    p = spend / total

    p = p[p > 0]

    return -(p * np.log2(p)).sum()

def create_credit_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create credit behaviour features.
    """

    # -------------------------------------------------
    # Available Credit
    # -------------------------------------------------

    df["available_credit"] = (
        df["f17"] - df["f1"]
    ).clip(lower=0)

    ENGINEERED_FEATURES["credit"].append("available_credit")

    # -------------------------------------------------
    # Available Consumer Credit
    # -------------------------------------------------

    df["available_consumer_credit"] = (
        df["f18"] - df["f1"]
    ).clip(lower=0)

    ENGINEERED_FEATURES["credit"].append(
        "available_consumer_credit"
    )

    # -------------------------------------------------
    # Revolving Utilization
    # -------------------------------------------------

    df["credit_utilization"] = (
        df["f1"] /
        (df["f17"] + EPSILON)
    )

    ENGINEERED_FEATURES["credit"].append(
        "credit_utilization"
    )

    # -------------------------------------------------
    # Consumer Utilization
    # -------------------------------------------------

    df["consumer_credit_utilization"] = (
        df["f1"] /
        (df["f18"] + EPSILON)
    )

    ENGINEERED_FEATURES["credit"].append(
        "consumer_credit_utilization"
    )

    # -------------------------------------------------
    # Spend Utilization
    # -------------------------------------------------

    df["spend_utilization"] = (
        df["f5"] /
        (df["f17"] + EPSILON)
    )

    ENGINEERED_FEATURES["credit"].append(
        "spend_utilization"
    )

    # -------------------------------------------------
    # Revolve vs Spend
    # -------------------------------------------------

    df["revolve_percentage"] = (
        df["f1"] /
        (df["f5"] + EPSILON)
    )

    ENGINEERED_FEATURES["credit"].append(
        "revolve_percentage"
    )

    # -------------------------------------------------
    # Credit Cushion
    # -------------------------------------------------

    df["credit_cushion"] = (
        df["available_credit"] /
        (df["f17"] + EPSILON)
    )

    ENGINEERED_FEATURES["credit"].append(
        "credit_cushion"
    )

    # -------------------------------------------------
    # Binary Features
    # -------------------------------------------------

    df["has_credit_line"] = (
        df["f17"] > 0
    ).astype("int8")

    ENGINEERED_FEATURES["credit"].append(
        "has_credit_line"
    )

    df["has_consumer_credit"] = (
        df["f18"] > 0
    ).astype("int8")

    ENGINEERED_FEATURES["credit"].append(
        "has_consumer_credit"
    )

    print(
        f"Created {len(ENGINEERED_FEATURES['credit'])} credit features."
    )

    return df