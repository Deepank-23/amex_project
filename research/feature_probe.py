"""
Feature Probe Engine
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import CONFIG
from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def probe_feature(
    feature: str,
    reference_model: str = "AMEX_R1_BEST_087",
):

    # -----------------------------
    # Load data
    # -----------------------------

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    submissions = load_submissions()

    reference = submissions[reference_model]

    # -----------------------------
    # Rank feature
    # -----------------------------

    probe = df[["ID", feature]].copy()

    probe["Prediction"] = (
        probe[feature]
        .rank(
            ascending=False,
            method="first",
        )
    )

    merged = probe.merge(
        reference,
        on="ID",
        suffixes=("_probe", "_reference"),
    )

    # -----------------------------
    # Correlations
    # -----------------------------

    pearson = merged["Prediction_probe"].corr(
        merged["Prediction_reference"],
        method="pearson",
    )

    spearman = merged["Prediction_probe"].corr(
        merged["Prediction_reference"],
        method="spearman",
    )

    # -----------------------------
    # Top20 overlap
    # -----------------------------

    k = int(len(merged) * 0.20)

    top_probe = set(
        merged.nsmallest(
            k,
            "Prediction_probe",
        )["ID"]
    )

    top_reference = set(
        merged.nsmallest(
            k,
            "Prediction_reference",
        )["ID"]
    )

    overlap = len(
        top_probe & top_reference
    ) / k

    print()

    print("=" * 80)
    print(feature)
    print("=" * 80)

    print(f"Pearson  : {pearson:.4f}")
    print(f"Spearman : {spearman:.4f}")
    print(f"Top20    : {overlap:.4%}")

    return {
        "Feature": feature,
        "Pearson": pearson,
        "Spearman": spearman,
        "Top20": overlap,
    }