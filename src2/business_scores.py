"""
NOT USING
"""

from __future__ import annotations

import pandas as pd


def create_revenue_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Revenue generating capability.
    """

    cols = [
        "f5_rank",
        "category_total_rank",
        "category_count_rank",
        "credit_utilization_rank",
    ]

    df["revenue_score"] = df[cols].mean(axis=1)

    return df


def create_interest_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interest earning opportunity.
    """

    cols = [
        "f1_rank",
        "credit_utilization_rank",
        "revolve_percentage_rank",
    ]

    df["interest_score"] = df[cols].mean(axis=1)

    return df


def create_engagement_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Customer engagement.
    """

    cols = [
        "f12_rank",
        "f22_rank",
        "f23_rank",
        "spending_entropy_rank",
    ]

    df["engagement_score"] = df[cols].mean(axis=1)

    return df


def create_reward_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reward program engagement.
    """

    cols = [
        "reward_breakage_rank",
        "reward_redemption_rate_rank",
        "reward_per_spend_rank",
    ]

    df["reward_score"] = df[cols].mean(axis=1)

    return df


def create_credit_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Credit relationship.
    """

    cols = [
        "credit_utilization_rank",
        "credit_cushion_rank",
        "available_credit_rank",
    ]

    df["credit_score"] = df[cols].mean(axis=1)

    return df


def create_all_business_scores(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df = create_revenue_score(df)

    df = create_interest_score(df)

    df = create_engagement_score(df)

    df = create_reward_score(df)

    df = create_credit_score(df)

    return df
