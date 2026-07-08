"""
Business Metrics Comparison
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import CONFIG
from src.economics import create_economics
from src.ltv import create_ltv
from research.submission_loader import load_submissions


REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def compare_business_metrics(
    baseline_model: str,
    experiment_model: str,
    top_percent: float = 0.20,
):

    # -----------------------------
    # Load data
    # -----------------------------

    data = pd.read_csv(CONFIG.train_path)

    if "id" in data.columns:
        data = data.rename(columns={"id": "ID"})

    data = create_economics(data)
    data = create_ltv(data)

    # -----------------------------
    # Load submissions
    # -----------------------------

    submissions = load_submissions()

    baseline = submissions[baseline_model].copy()

    baseline["Rank"] = (
        baseline["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    experiment = submissions[experiment_model].copy()

    experiment["Rank"] = (
        experiment["Prediction"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    baseline = baseline[["ID", "Rank"]].rename(
        columns={"Rank": "BaselineRank"}
    )

    experiment = experiment[["ID", "Rank"]].rename(
        columns={"Rank": "ExperimentRank"}
    )

    merged = (
        data
        .merge(baseline, on="ID")
        .merge(experiment, on="ID")
    )

    top_n = int(len(merged) * top_percent)

    baseline_top = merged[
        merged["BaselineRank"] <= top_n
    ]

    experiment_top = merged[
        merged["ExperimentRank"] <= top_n
    ]

    metrics = [
        "f1",
        "f5",
        "f11",
        "interest_revenue",
        "interchange_revenue",
        "rewards_breakage",
        "NetProfit",
        "LTV_Profitability",
    ]

    report = []

    for metric in metrics:

        base = baseline_top[metric].mean()
        exp = experiment_top[metric].mean()

        diff = exp - base

        if abs(base) > 1e-9:
            pct = 100 * diff / abs(base)
        else:
            pct = 0.0

        report.append(
            {
                "Metric": metric,
                "Baseline": base,
                "Experiment": exp,
                "Difference": diff,
                "PercentDifference": pct,
            }
        )

    report = pd.DataFrame(report)

    report.to_csv(
        REPORT_DIR /
        f"{baseline_model}_vs_{experiment_model}_business_metrics.csv",
        index=False,
    )

    print()
    print("=" * 80)
    print("BUSINESS METRICS")
    print("=" * 80)

    print(report.round(3).to_string(index=False))

    return report


if __name__ == "__main__":

    compare_business_metrics(
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
    )