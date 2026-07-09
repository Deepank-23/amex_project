"""
Derive Premium Engagement Weights
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPORT_DIR = Path("research/reports")


def derive_weights():

    df = pd.read_csv(
        REPORT_DIR / "customer_archetypes.csv"
    )

    features = [
        "f13",
        "f14",
        "f15",
        "f16",
        "f22",
        "f23",
    ]

    df = df[
        df["Feature"].isin(features)
    ].copy()

    df["Signal"] = (
        0.7*df["Agree_vs_None"].abs()+0.3*df["Best_vs_Agree"].abs()
    )

    df["Weight"] = (
        df["Signal"]
        / df["Signal"].sum()
    )

    df = df.sort_values(
        "Weight",
        ascending=False,
    )

    print()
    print("=" * 80)
    print("DERIVED PREMIUM WEIGHTS")
    print("=" * 80)

    print(
        df[
            [
                "Feature",
                "Signal",
                "Weight",
            ]
        ]
    )

    return df


if __name__ == "__main__":

    derive_weights()