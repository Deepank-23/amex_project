from __future__ import annotations

import pandas as pd


def create_submission(
    df: pd.DataFrame,
    score: pd.Series,
    path: str = "outputs/submissions/BEST_BASELINE.csv",
):

    submission = pd.DataFrame()

    if "ID" in df.columns:
        submission["ID"] = df["ID"]
    elif "id" in df.columns:
        submission["ID"] = df["id"]
    else:
        submission["ID"] = df.index

    submission["Prediction"] = (
        score.rank(
            ascending=False,
            method="first"
        ).astype(int)
    )   

    submission.to_csv(
        path,
        index=False,
    )

    print(f"\nSubmission saved to:\n{path}")

    return submission