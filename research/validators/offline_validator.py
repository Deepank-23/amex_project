"""
Offline Experiment Validation
"""

from __future__ import annotations

from research.validators.similarity import compare_similarity
from research.validators.customer_difference import analyze_customer_movement
from research.validators.feature_difference import analyze_feature_shift
from research.validators.business_metrics import compare_business_metrics
from research.validators.recommendation import generate_recommendation
from research.validators.rank_band import analyze_rank_bands
from research.validators.borderline import analyze_borderline

def validate_experiment(
    baseline_name: str,
    experiment_name: str,
) -> dict[str,object]:

    print("\n")
    print("=" * 80)
    print("OFFLINE EXPERIMENT VALIDATION")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("SIMILARITY")
    print("=" * 80)
    similarity = compare_similarity(
        baseline_name,
        experiment_name,
    )

    print("\n" + "=" * 80)
    print("CUSTOMER MOVEMENT")
    print("=" * 80)
    movement = analyze_customer_movement(
        baseline_name,
        experiment_name,
    )

    print("\n" + "=" * 80)
    print("BUSINESS METRICS")
    print("=" * 80)
    business = compare_business_metrics(
        baseline_name,
        experiment_name,
    )

    print("\n" + "=" * 80)
    print("FEATURE DIFFERENCE")
    print("=" * 80)
    features = analyze_feature_shift(
        baseline_name,
        experiment_name,
    )

    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    decision = generate_recommendation(
        similarity,
        movement,
        business["report"],
        features["report"],
    )

    print("\n" + "=" * 80)
    print("RANK BAND ANALYSIS")
    print("=" * 80)

    rank_bands = analyze_rank_bands(
        baseline_name,
        experiment_name,
    )
    print("\n" + "=" * 80)
    print("BORDERLINE ANALYSIS")
    print("=" * 80)

    borderline = analyze_borderline(
        baseline_name,
        experiment_name,
    )

    return {
        "similarity": similarity,

        "movement": {
            "entered_top20": int(movement["Entered_Top20"].sum()),
            "exited_top20": int(movement["Exited_Top20"].sum()),
        },

        "business": business["summary"],

        "features": features,

        "decision": decision,
        "rank_bands": rank_bands,
        "borderline": borderline
    }