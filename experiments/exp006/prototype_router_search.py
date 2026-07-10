"""
EXP006 Prototype Router Search

Scores customers by similarity to strong historical archetypes and distance from
weak disagreement archetypes.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.exp005.segment_router_search import (
    REFERENCE_MODELS,
    overlap_with_model,
    prepare_experiment_frame,
    proxy_objective,
    top20_ids,
    zscore,
)
from research.submission_loader import load_submissions
from src.submission import create_submission


EXPERIMENT_NAME = "EXP006_PROTOTYPE_ROUTER"
RESULT_PATH = Path("experiments/exp006/results.csv")
RAW_SCORE_PATH = Path("outputs/raw_scores/EXP006_PROTOTYPE_ROUTER_SCORE.csv")
SUBMISSION_PATH = Path("outputs/submissions/EXP006_PROTOTYPE_ROUTER.xlsx")

FEATURES = [
    "f1",
    "category_spend",
    "f11",
    "RetentionMultiplier",
    "benefit_count",
    "rewards_breakage_raw",
]


def add_router_features(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["rewards_breakage_raw"] = (
        enriched["f4"] - enriched["f21"]
    ).clip(lower=0)
    return enriched


def cluster_centroids(
    merged: pd.DataFrame,
) -> dict[str, pd.Series]:
    centroids: dict[str, pd.Series] = {}

    for cluster in [
        "ALL_THREE",
        "BEST_LTV",
        "BEST_ONLY",
        "LTV_ONLY",
        "PROFIT_ONLY",
    ]:
        centroids[cluster] = merged.loc[
            merged["Cluster"] == cluster,
            FEATURES,
        ].mean()

    return centroids


def weighted_distance(
    merged: pd.DataFrame,
    centroid: pd.Series,
    feature_weights: pd.Series,
) -> pd.Series:
    standardized = merged[FEATURES]
    delta = standardized.sub(centroid, axis=1)
    return ((delta ** 2) * feature_weights).sum(axis=1) ** 0.5


def run_search() -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = prepare_experiment_frame()
    merged = add_router_features(merged)
    merged = merged.astype({feature: "float64" for feature in FEATURES})

    standardized = merged[FEATURES].apply(zscore)
    merged.loc[:, FEATURES] = standardized

    centroids = cluster_centroids(merged)
    submissions = load_submissions(REFERENCE_MODELS)

    feature_weights = pd.Series(
        {
            "f1": 1.30,
            "category_spend": 1.30,
            "f11": 1.10,
            "RetentionMultiplier": 1.00,
            "benefit_count": 0.80,
            "rewards_breakage_raw": 0.90,
        }
    )

    rows: list[dict[str, float]] = []
    best_score = None
    best_meta = None

    distance_cache = {
        cluster: weighted_distance(merged, centroid, feature_weights)
        for cluster, centroid in centroids.items()
    }

    base_score = merged["BEST_Score"]

    for w_all, w_best_ltv, w_best_only, w_ltv_only, w_profit_only, w_base in product(
        [0.30, 0.40],
        [0.00, 0.10, 0.20],
        [0.00, 0.05, 0.10],
        [0.10, 0.15, 0.20],
        [0.10, 0.15, 0.20],
        [0.40, 0.50, 0.60],
    ):
        score = (
            w_base * zscore(base_score)
            - w_all * zscore(distance_cache["ALL_THREE"])
            - w_best_ltv * zscore(distance_cache["BEST_LTV"])
            - w_best_only * zscore(distance_cache["BEST_ONLY"])
            + w_ltv_only * zscore(distance_cache["LTV_ONLY"])
            + w_profit_only * zscore(distance_cache["PROFIT_ONLY"])
        )

        cluster_stats = proxy_objective(merged, score)

        row = {
            "AllThreeWeight": w_all,
            "BestLTVWeight": w_best_ltv,
            "BestOnlyWeight": w_best_only,
            "LTVOnlyPenalty": w_ltv_only,
            "ProfitOnlyPenalty": w_profit_only,
            "BaseWeight": w_base,
            **cluster_stats,
        }
        rows.append(row)

        if best_meta is None or row["Objective"] > best_meta["Objective"]:
            best_meta = row
            best_score = score

    results = pd.DataFrame(rows).sort_values(
        "Objective",
        ascending=False,
    )

    assert best_score is not None
    merged["EXP006_Score"] = best_score

    top_candidates = results.head(12).copy()
    overlap_rows = []

    for _, candidate in top_candidates.iterrows():
        score = (
            candidate["BaseWeight"] * zscore(base_score)
            - candidate["AllThreeWeight"] * zscore(distance_cache["ALL_THREE"])
            - candidate["BestLTVWeight"] * zscore(distance_cache["BEST_LTV"])
            - candidate["BestOnlyWeight"] * zscore(distance_cache["BEST_ONLY"])
            + candidate["LTVOnlyPenalty"] * zscore(distance_cache["LTV_ONLY"])
            + candidate["ProfitOnlyPenalty"] * zscore(distance_cache["PROFIT_ONLY"])
        )
        top20 = top20_ids(score, merged["ID"])
        overlap_rows.append(
            {
                "AllThreeWeight": candidate["AllThreeWeight"],
                "BestLTVWeight": candidate["BestLTVWeight"],
                "BestOnlyWeight": candidate["BestOnlyWeight"],
                "LTVOnlyPenalty": candidate["LTVOnlyPenalty"],
                "ProfitOnlyPenalty": candidate["ProfitOnlyPenalty"],
                "BaseWeight": candidate["BaseWeight"],
                "Overlap_BEST087": overlap_with_model(top20, submissions["AMEX_R1_BEST_087"]),
                "Overlap_LTV079": overlap_with_model(top20, submissions["AMEX_R1_LTV_Model_079"]),
                "Overlap_Profit077": overlap_with_model(top20, submissions["AMEX_R1_NetProfit_Model_077"]),
            }
        )

    overlap_report = pd.DataFrame(overlap_rows)
    results = results.merge(
        overlap_report,
        on=[
            "AllThreeWeight",
            "BestLTVWeight",
            "BestOnlyWeight",
            "LTVOnlyPenalty",
            "ProfitOnlyPenalty",
            "BaseWeight",
        ],
        how="left",
    )

    return merged, results


def save_outputs(merged: pd.DataFrame, results: pd.DataFrame) -> None:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUBMISSION_PATH.parent.mkdir(parents=True, exist_ok=True)

    results.to_csv(RESULT_PATH, index=False)

    pd.DataFrame(
        {
            "ID": merged["ID"],
            "Prediction": merged["EXP006_Score"],
        }
    ).to_csv(RAW_SCORE_PATH, index=False)

    create_submission(
        df=merged,
        score=merged["EXP006_Score"],
        path=SUBMISSION_PATH,
        framework=build_framework(results.iloc[0]),
    )


def build_framework(best_row: pd.Series) -> dict[str, str]:
    return {
        "Variables Used": (
            "Core BEST087 components plus prototype-matching features built "
            "from f1, category_spend, f11, RetentionMultiplier, benefit_count, "
            "and rewards_breakage_raw."
        ),
        "Profitability Equation": (
            "EXP006_Score = "
            f"{best_row['BaseWeight']:.2f}*z(BEST087) - "
            f"{best_row['AllThreeWeight']:.2f}*z(dist_to_ALL_THREE) - "
            f"{best_row['BestLTVWeight']:.2f}*z(dist_to_BEST_LTV) - "
            f"{best_row['BestOnlyWeight']:.2f}*z(dist_to_BEST_ONLY) + "
            f"{best_row['LTVOnlyPenalty']:.2f}*z(dist_to_LTV_ONLY) + "
            f"{best_row['ProfitOnlyPenalty']:.2f}*z(dist_to_PROFIT_ONLY)."
        ),
        "Prediction Logic": (
            "The score ranks customers higher when they resemble the strongest "
            "shared historical archetypes and lower when they resemble the "
            "known one-sided disagreement archetypes."
        ),
        "Variable Selection Logic": (
            "Prototype features come directly from EXP004 disagreement "
            "clusters. ALL_THREE and BEST_LTV represent good target archetypes; "
            "LTV_ONLY and PROFIT_ONLY represent failure modes."
        ),
        "Coefficient/Weight Derivation": (
            "Weights were chosen by grid search using the same cluster-based "
            "reverse-engineered proxy objective. Best row: "
            f"all_three={best_row['AllThreeWeight']:.2f}, "
            f"best_ltv={best_row['BestLTVWeight']:.2f}, "
            f"best_only={best_row['BestOnlyWeight']:.2f}, "
            f"ltv_only_penalty={best_row['LTVOnlyPenalty']:.2f}, "
            f"profit_only_penalty={best_row['ProfitOnlyPenalty']:.2f}, "
            f"base={best_row['BaseWeight']:.2f}."
        ),
        "Feature Transformations": (
            "Selected prototype features are standardized, then customer-to-"
            "prototype weighted Euclidean distances are computed and z-scored "
            "before combining."
        ),
        "Business Logic": (
            "A customer should score well if they look like the shared winning "
            "archetypes, not merely if they optimize a single business lens."
        ),
        "Assumptions": (
            "Historical winners encode latent customer segments. Distance to "
            "those segments is a better guide than adding flat scalar bonuses."
        ),
        "Validation Approach": (
            "Validated through disagreement-cluster objective search and "
            "historical overlap checks against BEST087, LTV079, and "
            "NetProfit077."
        ),
        "Additional Notes (Optional)": (
            "This is the more aggressive, higher-variance prototype-based "
            "submission in the current experiment family."
        ),
    }


def main() -> None:
    merged, results = run_search()
    save_outputs(merged, results)

    print()
    print("=" * 80)
    print(EXPERIMENT_NAME)
    print("=" * 80)
    print(results.head(15).round(4).to_string(index=False))


if __name__ == "__main__":
    main()
