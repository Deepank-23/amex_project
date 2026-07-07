"""
Debug Utilities
"""

import pandas as pd


def check_missing(df: pd.DataFrame):

    print("\n")
    print("=" * 80)
    print("MISSING VALUE REPORT")
    print("=" * 80)

    missing = df.isna().sum()

    missing = missing[missing > 0]

    if len(missing) == 0:
        print("✓ No missing values remain.")
    else:
        print(missing)