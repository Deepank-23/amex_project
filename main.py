"""
AMEX R2

Baseline Pipeline
"""

from src.economics import create_economics
from src.ltv import create_ltv
from src.evidence import create_evidence
from src.baseline087 import create_best087_score
from src.config import CONFIG
from src.preprocessing import (
    preprocess_baseline,
    preprocess_research,
)
from src.submission import (
    create_submission,
    save_raw_scores,
)
from src.validation import validate_components
from src.baseline_validation import validate_raw_scores
def main():

    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)

    if CONFIG.baseline_mode:
        print("Running BASELINE pipeline")
        df = preprocess_baseline()
    else:
        print("Running RESEARCH pipeline")
        df = preprocess_research()   
    print("\nMissing Values")
    print("-" * 40)
    missing = df.isna().sum()

    missing = missing[missing > 0]

    print(missing) 
    print(df.shape)

    print("\n")

    print("=" * 80)
    print("ECONOMICS")
    print("=" * 80)

    
    df = create_economics(df)


    print(df.shape)

    print("\n")

    print("=" * 80)
    print("LTV")
    print("=" * 80)

    df = create_ltv(df)

    print(df.shape)

    print("\n")

    print("=" * 80)
    print("EVIDENCE")
    print("=" * 80)

    df = create_evidence(df)

    print(df.shape)

    print("\n")

    print("=" * 80)
    print("BEST 0.87")
    print("=" * 80)

    df = create_best087_score(df)

    print(df["BEST_Score"].describe())

    print("\n")

    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)

    validate_components(df)

    print("\n")

    print("=" * 80)
    print("SUBMISSION")
    print("=" * 80)
    submission = create_submission(
        df=df,
        score=df["BEST_Score"],
        path="outputs/submissions/BEST_BASELINE.csv",
    )
    raw_scores = save_raw_scores(df)
    

    validate_raw_scores(
        current_path="outputs/raw_scores/BEST_BASELINE_SCORE.csv",
        historical_path="data/previous_submission/AMEX_R1_BEST_087.xlsx",
    )

    print(submission.head())

    print("\nDone.")

    return submission


if __name__ == "__main__":
    main()