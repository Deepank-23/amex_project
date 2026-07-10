"""
EXP004 Disagreement Cluster Analysis

This experiment profiles where the strongest historical submissions disagree.
It does not create a new scoring model; it extracts evidence for the next
business hypothesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.submission_loader import load_submissions
from src.economics import create_economics
from src.ltv import create_ltv
from src.preprocessing import preprocess_baseline


@dataclass(frozen=True)
class Exp004Config:
    experiment_id: str = "EXP004"
    name: str = "EXP004_DISAGREEMENT_CLUSTERS"
    top_percent: float = 0.20
    models: tuple[str, ...] = (
        "AMEX_R1_BEST_087",
        "AMEX_R1_LTV_Model_079",
        "AMEX_R1_NetProfit_Model_077",
    )
    output_dir: Path = Path("research/reports/exp004")
    result_path: Path = Path("experiments/exp004/results.csv")


CONFIG = Exp004Config()


PROFILE_COLUMNS = [
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f11",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f19",
    "f20",
    "f22",
    "f23",
    "category_spend",
    "interest_revenue",
    "interchange_revenue",
    "rewards_breakage",
    "expected_credit_loss",
    "benefit_cost",
    "servicing_cost",
    "NetProfit",
    "benefit_count",
    "RetentionMultiplier",
    "LTV_Profitability",
]


def prepare_customer_data() -> pd.DataFrame:
    df = preprocess_baseline()
    df = create_economics(df)
    df = create_ltv(df)
    return df


def normalize_submission(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()

    if "id" in normalized.columns:
        normalized = normalized.rename(columns={"id": "ID"})

    if "prediction" in normalized.columns:
        normalized = normalized.rename(columns={"prediction": "Prediction"})

    required = {"ID", "Prediction"}
    missing = required.difference(normalized.columns)

    if missing:
        raise ValueError(f"Submission missing columns: {sorted(missing)}")

    return normalized[["ID", "Prediction"]]


def add_model_flags(
    data: pd.DataFrame,
    submissions: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    merged = data[["ID"]].copy()
    top_n = int(len(data) * CONFIG.top_percent)

    for model in CONFIG.models:
        submission = normalize_submission(submissions[model])
        ranked = submission.sort_values(
            "Prediction",
            ascending=False,
        ).reset_index(drop=True)

        top_ids = set(ranked.head(top_n)["ID"])
        rank_map = pd.Series(
            ranked.index + 1,
            index=ranked["ID"],
        )

        short_name = model_short_name(model)
        merged[f"{short_name}_Top20"] = merged["ID"].isin(top_ids)
        merged[f"{short_name}_Rank"] = merged["ID"].map(rank_map)

    return merged


def model_short_name(model: str) -> str:
    if "BEST" in model:
        return "BEST"
    if "LTV" in model:
        return "LTV"
    if "NetProfit" in model:
        return "PROFIT"
    return model


def assign_cluster(row: pd.Series) -> str:
    flags = {
        "BEST": bool(row["BEST_Top20"]),
        "LTV": bool(row["LTV_Top20"]),
        "PROFIT": bool(row["PROFIT_Top20"]),
    }

    selected = [name for name, flag in flags.items() if flag]

    if len(selected) == 3:
        return "ALL_THREE"

    if len(selected) == 0:
        return "NONE"

    if len(selected) == 1:
        return f"{selected[0]}_ONLY"

    return "_".join(selected)


def summarize_clusters(
    merged: pd.DataFrame,
) -> pd.DataFrame:
    population = merged[PROFILE_COLUMNS].mean(numeric_only=True)
    rows = []

    for cluster, group in merged.groupby("Cluster"):
        row = {
            "Cluster": cluster,
            "Customers": len(group),
            "PopulationShare": len(group) / len(merged),
        }

        for col in PROFILE_COLUMNS:
            mean_value = group[col].mean()
            row[f"{col}_Mean"] = mean_value

            base = population[col]
            if abs(base) > 1e-9:
                row[f"{col}_LiftVsPopulation"] = mean_value / base
            else:
                row[f"{col}_LiftVsPopulation"] = 0.0

        rows.append(row)

    return pd.DataFrame(rows).sort_values(
        ["Customers", "Cluster"],
        ascending=[False, True],
    )


def summarize_pairwise_segments(
    merged: pd.DataFrame,
) -> pd.DataFrame:
    pairs = [
        ("BEST", "LTV"),
        ("BEST", "PROFIT"),
        ("LTV", "PROFIT"),
    ]
    rows = []

    for left, right in pairs:
        left_flag = merged[f"{left}_Top20"]
        right_flag = merged[f"{right}_Top20"]

        segments = {
            "BOTH": left_flag & right_flag,
            f"{left}_ONLY": left_flag & ~right_flag,
            f"{right}_ONLY": ~left_flag & right_flag,
            "NEITHER": ~left_flag & ~right_flag,
        }

        for segment, mask in segments.items():
            group = merged[mask]
            row = {
                "Pair": f"{left}_vs_{right}",
                "Segment": segment,
                "Customers": len(group),
                "PopulationShare": len(group) / len(merged),
            }

            for col in PROFILE_COLUMNS:
                row[f"{col}_Mean"] = group[col].mean()

            rows.append(row)

    return pd.DataFrame(rows)


def rank_delta_correlations(
    merged: pd.DataFrame,
) -> pd.DataFrame:
    pairs = [
        ("BEST", "LTV"),
        ("BEST", "PROFIT"),
        ("LTV", "PROFIT"),
    ]
    rows = []

    for left, right in pairs:
        delta_name = f"{left}_minus_{right}_RankDelta"
        merged[delta_name] = (
            merged[f"{left}_Rank"]
            - merged[f"{right}_Rank"]
        )

        for col in PROFILE_COLUMNS:
            rows.append(
                {
                    "Pair": f"{left}_vs_{right}",
                    "Feature": col,
                    "SpearmanWithRankDelta": merged[
                        [delta_name, col]
                    ].corr(method="spearman").iloc[0, 1],
                }
            )

    report = pd.DataFrame(rows)

    return report.sort_values(
        "SpearmanWithRankDelta",
        key=lambda series: series.abs(),
        ascending=False,
    )


def build_results_summary(
    cluster_summary: pd.DataFrame,
    rank_corr: pd.DataFrame,
) -> pd.DataFrame:
    focus_clusters = [
        "BEST_ONLY",
        "LTV_ONLY",
        "PROFIT_ONLY",
        "BEST_LTV",
        "BEST_PROFIT",
        "LTV_PROFIT",
        "ALL_THREE",
    ]

    rows = []

    for cluster in focus_clusters:
        subset = cluster_summary[
            cluster_summary["Cluster"] == cluster
        ]

        if subset.empty:
            continue

        row = subset.iloc[0]
        rows.append(
            {
                "Cluster": cluster,
                "Customers": int(row["Customers"]),
                "SpendLift": row["category_spend_LiftVsPopulation"],
                "RevolveLift": row["f1_LiftVsPopulation"],
                "RiskLift": row["f11_LiftVsPopulation"],
                "ProfitLift": row["NetProfit_LiftVsPopulation"],
                "LTVLift": row["LTV_Profitability_LiftVsPopulation"],
            }
        )

    summary = pd.DataFrame(rows)
    if not rank_corr.empty:
        top_signal = rank_corr.head(1).iloc[0]
        summary["TopRankDeltaPair"] = top_signal["Pair"]
        summary["TopRankDeltaSignal"] = top_signal["Feature"]
    else:
        summary["TopRankDeltaPair"] = ""
        summary["TopRankDeltaSignal"] = ""

    return summary


def run() -> dict[str, pd.DataFrame]:
    CONFIG.output_dir.mkdir(parents=True, exist_ok=True)
    CONFIG.result_path.parent.mkdir(parents=True, exist_ok=True)

    data = prepare_customer_data()
    submissions = load_submissions(CONFIG.models)
    flags = add_model_flags(data, submissions)

    merged = data.merge(flags, on="ID")
    merged["Cluster"] = merged.apply(assign_cluster, axis=1)

    cluster_summary = summarize_clusters(merged)
    pairwise_summary = summarize_pairwise_segments(merged)
    rank_corr = rank_delta_correlations(merged)
    results = build_results_summary(cluster_summary, rank_corr)

    merged[
        [
            "ID",
            "Cluster",
            "BEST_Top20",
            "LTV_Top20",
            "PROFIT_Top20",
            "BEST_Rank",
            "LTV_Rank",
            "PROFIT_Rank",
        ]
    ].to_csv(CONFIG.output_dir / "customer_disagreement_clusters.csv", index=False)

    cluster_summary.to_csv(
        CONFIG.output_dir / "cluster_feature_lifts.csv",
        index=False,
    )
    pairwise_summary.to_csv(
        CONFIG.output_dir / "pairwise_segment_summary.csv",
        index=False,
    )
    rank_corr.to_csv(
        CONFIG.output_dir / "rank_delta_correlations.csv",
        index=False,
    )
    results.to_csv(CONFIG.result_path, index=False)

    print()
    print("=" * 80)
    print(CONFIG.name)
    print("=" * 80)
    print("Cluster counts")
    print(merged["Cluster"].value_counts().to_string())
    print()
    print("Results summary")
    print(results.round(3).to_string(index=False))
    print()
    print("Top rank-delta signals")
    print(rank_corr.head(15).round(4).to_string(index=False))

    return {
        "clusters": cluster_summary,
        "pairwise": pairwise_summary,
        "rank_delta": rank_corr,
        "results": results,
    }


if __name__ == "__main__":
    run()
