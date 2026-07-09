"""
Customer Consensus Analysis
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import sys


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CONFIG
from research.submission_loader import load_submissions

REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def build_consensus(
    models: list[str],
    top_percent: float = 0.20,
):

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    submissions = load_submissions()

    consensus = df[["ID"]].copy()

    for model in models:

        submission = submissions[model]

        k = int(len(submission) * top_percent)

        top_ids = set(
            submission.nlargest(
                k,
                "Prediction",
            )["ID"]
        )

        consensus[model] = (
            consensus["ID"]
            .isin(top_ids)
            .astype(int)
        )

    return consensus

def assign_group(row):

    total = row.sum()

    if total == 3:
        return "ALL_AGREE"

    if total == 0:
        return "NONE"

    if row.iloc[0]:
        return "BEST_ONLY"

    if row.iloc[1]:
        return "LTV_ONLY"

    if row.iloc[2]:
        return "PROFIT_ONLY"

    return "MIXED"

def compare_groups(
    consensus: pd.DataFrame,
):

    df = pd.read_csv(CONFIG.train_path)

    if "id" in df.columns:
        df = df.rename(columns={"id": "ID"})

    merged = df.merge(
        consensus[["ID", "Group"]],
        on="ID",
    )

    features = [
        col
        for col in merged.columns
        if col.startswith("f")
    ]

    report = []

    groups = [
        "ALL_AGREE",
        "BEST_ONLY",
        "LTV_ONLY",
        "PROFIT_ONLY",
        "NONE",
    ]

    for feature in features:

        row = {
            "Feature": feature,
        }

        for group in groups:

            subset = merged[
                merged["Group"] == group
            ]

            row[f"{group}_Mean"] = subset[
                feature
            ].mean()

            row[f"{group}_Median"] = subset[
                feature
            ].median()

            row[f"{group}_P75"] = subset[
                feature
            ].quantile(0.75)

            row[f"{group}_P90"] = subset[
                feature
            ].quantile(0.90)

        report.append(row)

    report = pd.DataFrame(report)

    report.to_csv(
        REPORT_DIR / "group_feature_summary.csv",
        index=False,
    )

    print()
    print("=" * 100)
    print("GROUP FEATURE SUMMARY")
    print("=" * 100)

    print(report)

    return report



def find_discriminative_features(
    group_report: pd.DataFrame,
):

    groups = [
        "ALL_AGREE",
        "BEST_ONLY",
        "LTV_ONLY",
        "PROFIT_ONLY",
        "NONE",
    ]

    report = []

    for _, row in group_report.iterrows():

        feature = row["Feature"]

        means = [
            row[f"{group}_Mean"]
            for group in groups
        ]

        maximum = max(means)
        minimum = min(means)

        report.append(
            {
                "Feature": feature,
                "Range": maximum - minimum,
                "Std": pd.Series(means).std(),
                "MaxGroup": groups[
                    means.index(maximum)
                ],
                "MinGroup": groups[
                    means.index(minimum)
                ],
            }
        )

    report = pd.DataFrame(report)

    report = report.sort_values(
        "Range",
        ascending=False,
    )

    report.to_csv(
        REPORT_DIR / "feature_importance_by_groups.csv",
        index=False,
    )

    print()
    print("=" * 100)
    print("MOST DISCRIMINATIVE FEATURES")
    print("=" * 100)

    print(report)

    return report

def build_archetypes(
    group_summary: pd.DataFrame,
):

    report = group_summary.copy()

    report["Agree_vs_None"] = (
        report["ALL_AGREE_Mean"]
        - report["NONE_Mean"]
    )

    report["Best_vs_Agree"] = (
        report["BEST_ONLY_Mean"]
        - report["ALL_AGREE_Mean"]
    )

    report["LTV_vs_Agree"] = (
        report["LTV_ONLY_Mean"]
        - report["ALL_AGREE_Mean"]
    )

    report["Profit_vs_Agree"] = (
        report["PROFIT_ONLY_Mean"]
        - report["ALL_AGREE_Mean"]
    )

    report.to_csv(
        REPORT_DIR / "customer_archetypes.csv",
        index=False,
    )

    print()
    print("=" * 100)
    print("CUSTOMER ARCHETYPES")
    print("=" * 100)

    print(
        report[
            [
                "Feature",
                "Agree_vs_None",
                "Best_vs_Agree",
                "LTV_vs_Agree",
                "Profit_vs_Agree",
            ]
        ]
    )

    return report

if __name__ == "__main__":

    MODELS = [
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
        "AMEX_R1_NetProfit_Model_077",
    ]

    consensus = build_consensus(MODELS)

    consensus["Group"] = (
        consensus[
            MODELS
        ].apply(assign_group, axis=1)
    )

    consensus.to_csv(
        REPORT_DIR / "customer_consensus.csv",
        index=False,
    )

    print()
    print("=" * 80)
    print("CUSTOMER GROUPS")
    print("=" * 80)

    print(
        consensus["Group"].value_counts()
    )
    summary = compare_groups(
        consensus,
    )

    find_discriminative_features(
        summary,
    )
    build_archetypes(summary)

