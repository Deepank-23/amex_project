"""
Feature Probe Engine
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

# ---------------------------------------------------------
# Consensus Probe
# ---------------------------------------------------------

def probe_consensus(
    feature: str,
    models: list[str],
    top_percent: float = 0.20,
):

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    submissions = load_submissions()

    dataset_mean = df[feature].mean()

    results = {
        "Feature": feature,
        "DatasetMean": dataset_mean,
    }

    print()
    print("=" * 80)
    print(f"CONSENSUS PROBE : {feature}")
    print("=" * 80)
    print(f"Dataset Mean : {dataset_mean:.4f}")

    for model in models:

        submission = submissions[model]

        merged = df.merge(
            submission,
            on="ID",
        )

        k = int(len(merged) * top_percent)

        top = merged.nlargest(
            k,
            "Prediction",
        )

        top_mean = top[feature].mean()

        lift = (
            (top_mean - dataset_mean)
            / abs(dataset_mean)
            * 100
            if dataset_mean != 0
            else 0
        )

        results[model] = lift

        print(
            f"{model:35s} "
            f"{lift:8.2f}%"
        )

    model_lifts = [
        results[m]
        for m in models
    ]

    consensus = sum(model_lifts) / len(model_lifts)

    results["Consensus"] = consensus

    print("-" * 80)
    print(f"Consensus Lift : {consensus:.2f}%")

    return results

# ---------------------------------------------------------
# Probe Multiple Features
# ---------------------------------------------------------

def probe_all_features(
    features: list[str],
    models: list[str],
    top_percent: float = 0.20,
):

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    submissions = load_submissions()

    report = []

    for feature in features:

        dataset_mean = df[feature].mean()
        dataset_median = df[feature].median()
        dataset_p75 = df[feature].quantile(0.75)
        dataset_p90 = df[feature].quantile(0.90)

        row = {
            "Feature": feature,
            "DatasetMean": dataset_mean,
            "DatasetMedian": dataset_median,
            "DatasetP75": dataset_p75,
            "DatasetP90": dataset_p90,
        }
        mean_lifts = []
        median_lifts = []

        for model in models:

            submission = submissions[model]

            merged = df.merge(
                submission,
                on="ID",
            )

            k = int(len(merged) * top_percent)

            top = merged.nlargest(
                k,
                "Prediction",
            )

            top_mean = top[feature].mean()
            top_median = top[feature].median()

            top_p75 = top[feature].quantile(0.75)
            top_p90 = top[feature].quantile(0.90)

            mean_lift = (
                (top_mean - dataset_mean)
                / abs(dataset_mean)
                * 100
                if dataset_mean != 0
                else 0
            )

            median_lift = (
                (top_median - dataset_median)
                / abs(dataset_median)
                * 100
                if dataset_median != 0
                else 0
            )

            row[f"{model}_Mean"] = top_mean
            row[f"{model}_Median"] = top_median
            row[f"{model}_P75"] = top_p75
            row[f"{model}_P90"] = top_p90

            row[f"{model}_MeanLift"] = mean_lift
            row[f"{model}_MedianLift"] = median_lift

            mean_lifts.append(mean_lift)
            median_lifts.append(median_lift)

        consensus_mean = sum(mean_lifts) / len(mean_lifts)
        consensus_median = sum(median_lifts) / len(median_lifts)

        row["ConsensusMean"] = consensus_mean
        row["ConsensusMedian"] = consensus_median

        row["Direction"] = (
            "Higher"
            if consensus_mean > 0
            else "Lower"
        )

        report.append(row)

    report = pd.DataFrame(report)

    report = report.sort_values(
        "ConsensusMean",
        ascending=False,
    )

    report.to_csv(
        REPORT_DIR / "feature_consensus_report.csv",
        index=False,
    )

    print()
    print("=" * 120)
    print("FEATURE CONSENSUS REPORT")
    print("=" * 120)

    print(
        report[
            [
                "Feature",
                "DatasetMean",
                "DatasetMedian",
                "DatasetP75",
                "DatasetP90",
                "ConsensusMean",
                "ConsensusMedian",
                "Direction",
            ]
        ]
    )
    return report

if __name__ == "__main__":

    FEATURES = [
        f"f{i}"
        for i in range(1,24)
    ]

    MODELS = [
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
        "AMEX_R1_NetProfit_Model_077",
    ]

    probe_all_features(
        FEATURES,
        MODELS,
    )