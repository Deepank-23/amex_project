from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import CONFIG
from src.constants import (
    LOG_FEATURES,
    RANK_FEATURES,
    BINARY_FEATURES,
    MISSING_THRESHOLD,
    LOWER_CLIP,
    UPPER_CLIP,
    EPSILON
)

def load_data() -> pd.DataFrame:

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    return df

def validate_data(df: pd.DataFrame) -> None:
    """
    Basic validation checks.
    """

    print("=" * 40)

    print("Shape :", df.shape)

    print("Duplicate Rows :", df.duplicated().sum())

    print("Duplicate IDs :", df["ID"].duplicated().sum())

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

            # Floor impossible inputs just above -1 to avoid log1p warnings.
            df[f"{col}_log"] = np.log1p(df[col].clip(lower=-1 + EPSILON))

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
def preprocess_research() -> pd.DataFrame:

    df = load_data()

    validate_data(df)

    df = create_missing_flags(df)

    df = fill_structural_missing(df)

    df = clip_outliers(df)

    df = log_transform(df)

    df = rank_transform(df)

    return df

def preprocess_baseline() -> pd.DataFrame:

    df = load_data()

    validate_data(df)

    zero_impute_cols = [
        "f4","f6","f7","f8","f9","f10",
        "f13","f14","f15","f16",
        "f17","f18","f21"
    ]

    for c in zero_impute_cols:
        df[c] = df[c].fillna(0)

    df["f5"] = df["f5"].fillna(df["f5"].median())
    df["f11"] = df["f11"].fillna(df["f11"].median())
    df["f12"] = df["f12"].fillna(0)
    df["f19"] = df["f19"].fillna(0)
    df["f20"] = df["f20"].fillna(0)
    df["f22"] = df["f22"].fillna(0)
    df["f23"] = df["f23"].fillna(0)

    print("\nRemaining Missing Values")

    print(df.isna().sum())

    return df