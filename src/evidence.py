"""
Evidence Layer

Creates the evidence-weighted ranking features.
"""

from __future__ import annotations

import pandas as pd


# -------------------------------------------------------
# Standalone Probe Results
# -------------------------------------------------------

LIFT_RESULTS = {

    "Spend": 66.8,

    "Revolving": 54.9,

    "Breakage": 31.7,

}

BASELINE = 20.0


def create_evidence(df: pd.DataFrame) -> pd.DataFrame:


    # ---------------------------------------
    # Evidence Lift
    # ---------------------------------------

    lift_spend = LIFT_RESULTS["Spend"] - BASELINE

    lift_f1 = LIFT_RESULTS["Revolving"] - BASELINE

    lift_breakage = LIFT_RESULTS["Breakage"] - BASELINE

    total = (

        lift_spend

        + lift_f1

        + lift_breakage

    )

    w_spend = lift_spend / total

    w_f1 = lift_f1 / total

    w_breakage = lift_breakage / total

    print("\nEvidence Weights")

    print(f"Spend      : {w_spend:.3f}")

    print(f"Revolving  : {w_f1:.3f}")

    print(f"Breakage   : {w_breakage:.3f}")

    # ---------------------------------------
    # Raw Breakage
    # ---------------------------------------

    df["rewards_breakage_raw"] = (

        df["f4"]

        - df["f21"]

    ).clip(lower=0)

    # ---------------------------------------
    # Percentile Ranks
    # ---------------------------------------

    df["rank_spend"] = (

        df["category_spend"]

        .rank(pct=True)

    )

    df["rank_f1"] = (

        df["f1"]

        .rank(pct=True)

    )

    df["rank_breakage"] = (

        df["rewards_breakage_raw"]

        .rank(pct=True)

    )

    # ---------------------------------------
    # Evidence Score
    # ---------------------------------------

    df["Score_v2"] = (

        w_spend * df["rank_spend"]

        + w_f1 * df["rank_f1"]

        + w_breakage * df["rank_breakage"]

    )
    print(df["Score_v2"].describe())
    return df

