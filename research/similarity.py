"""
Submission Similarity Matrix
"""

from __future__ import annotations

import pandas as pd

from submission_loader import load_submissions
from overlap import compare_submissions
from pathlib import Path

REPORT_DIR = Path("research/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def similarity_matrix():

    submissions = load_submissions()

    names = list(submissions.keys())

    pearson = pd.DataFrame(
        index=names,
        columns=names,
        dtype=float,
    )

    spearman = pd.DataFrame(
        index=names,
        columns=names,
        dtype=float,
    )

    top20 = pd.DataFrame(
        index=names,
        columns=names,
        dtype=float,
    )

    for i, name1 in enumerate(names):

        for j, name2 in enumerate(names):

            if j < i:
                continue

            df1 = submissions[name1]
            df2 = submissions[name2]

            merged = df1.merge(
                df2,
                on="ID",
                suffixes=("_1", "_2"),
            )

            p = merged["Prediction_1"].corr(
                merged["Prediction_2"],
                method="pearson",
            )

            s = merged["Prediction_1"].corr(
                merged["Prediction_2"],
                method="spearman",
            )

            k = int(len(merged) * 0.20)

            top1 = set(
                merged.nsmallest(
                    k,
                    "Prediction_1",
                )["ID"]
            )

            top2 = set(
                merged.nsmallest(
                    k,
                    "Prediction_2",
                )["ID"]
            )

            overlap = len(top1 & top2) / k

            pearson.loc[name1, name2] = p
            pearson.loc[name2, name1] = p

            spearman.loc[name1, name2] = s
            spearman.loc[name2, name1] = s

            top20.loc[name1, name2] = overlap
            top20.loc[name2, name1] = overlap

    return pearson, spearman, top20


if __name__ == "__main__":

    pearson, spearman, overlap = similarity_matrix()

    print()

    print("=" * 80)
    print("PEARSON")
    print("=" * 80)

    print(pearson.round(4))

    print()

    print("=" * 80)
    print("SPEARMAN")
    print("=" * 80)

    print(spearman.round(4))

    print()

    print("=" * 80)
    print("TOP20 OVERLAP")
    print("=" * 80)

    print(overlap.round(4))

    pearson.to_csv(REPORT_DIR / "pearson_matrix.csv")
    spearman.to_csv(REPORT_DIR / "spearman_matrix.csv")
    overlap.to_csv(REPORT_DIR / "top20_overlap.csv")