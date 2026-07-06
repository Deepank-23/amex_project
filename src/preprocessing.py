from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import TRAIN_PATH
from src.constants import (
    LOG_FEATURES,
    RANK_FEATURES,
    BINARY_FEATURES,
    MISSING_THRESHOLD,
    LOWER_CLIP,
    UPPER_CLIP
)

def load_data() -> pd.DataFrame:
    """
    Load dataset.
    """

    df = pd.read_csv(TRAIN_PATH)

    return df

def validate_data(df: pd.DataFrame) -> None:
    """
    Basic validation checks.
    """

    print("=" * 40)

    print("Shape :", df.shape)

    print("Duplicate Rows :", df.duplicated().sum())

    print("Duplicate IDs :", df["id"].duplicated().sum())

    print("=" * 40)

def create_missing_flags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create binary indicators for columns with significant missing values.
    """

    missing_percent = df.isnull().mean()

    missing_cols = missing_percent[
        missing_percent > MISSING_THRESHOLD
    ].index.tolist()

    for col in missing_cols:
        df[f"{col}_missing"] = df[col].isna().astype("int8")

    print(f"Created {len(missing_cols)} missing indicators.")

    return df

def fill_structural_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill structural missing values with 0.
    Missing indicators preserve the information.
    """

    missing_before = df.isna().sum().sum()

    df = df.fillna(0)

    missing_after = df.isna().sum().sum()

    print(f"Missing Before : {missing_before}")
    print(f"Missing After  : {missing_after}")

    return df



def clip_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clip extreme values using quantiles.
    """

    numeric_cols = df.select_dtypes(include="number").columns

    # Don't clip ID or binary columns
    skip_cols = ["ID"] + BINARY_FEATURES

    for col in numeric_cols:

        if col in skip_cols:
            continue

        lower = df[col].quantile(LOWER_CLIP)
        upper = df[col].quantile(UPPER_CLIP)

        df[col] = df[col].clip(lower=lower, upper=upper)

    print("✓ Outliers clipped")

    return df

def log_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply log1p transformation.
    """

    for col in LOG_FEATURES:

        if col in df.columns:

            df[f"{col}_log"] = np.log1p(df[col])

    print("✓ Log features created")

    return df

def rank_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create percentile rank features.
    """

    for col in RANK_FEATURES:

        if col in df.columns:

            df[f"{col}_rank"] = df[col].rank(pct=True)

    print("✓ Rank features created")

    return df

def preprocess() -> pd.DataFrame:

    df = load_data()

    validate_data(df)

    df = create_missing_flags(df)

    df = fill_structural_missing(df)

    df = clip_outliers(df)

    df = log_transform(df)

    df = rank_transform(df)

    return df