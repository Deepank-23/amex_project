"""
Offline Experiment Validation
"""

from __future__ import annotations

from research.validators.similarity import compare_similarity
from research.validators.customer_difference import analyze_customer_movement
from research.validators.feature_difference import analyze_feature_shift
from research.validators.business_metrics import compare_business_metrics
from research.validators.recommendation import generate_recommendation


def validate_experiment(
    baseline_name: str,
    experiment_name: str,
) :

    print("\n")
    print("=" * 80)
    print("OFFLINE EXPERIMENT VALIDATION")
    print("=" * 80)

    similarity = compare_similarity(
        baseline_name,
        experiment_name,
    )
    print("=" * 80)
    print("SIMILARITY")
    print("=" * 80)


    movement = analyze_customer_movement(
        baseline_name,
        experiment_name,
    )
    print("=" * 80)
    print("SIMILARITY")
    print("=" * 80)

    business = compare_business_metrics(
        baseline_name,
        experiment_name,
    )
    print("=" * 80)
    print("SIMILARITY")
    print("=" * 80)

    features = analyze_feature_shift(
        baseline_name,
        experiment_name,
    )

    print("=" * 80)
    print("SIMILARITY")
    print("=" * 80)

    generate_recommendation(
        similarity,
        movement,
        business,
        features,
    )