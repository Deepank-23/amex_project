"""
EXP003A - Conditional Premium Threshold Search
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from main import main
from src.config import CONFIG


THRESHOLDS = [
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
]

results = []


for threshold in THRESHOLDS:

    print("\n")
    print("=" * 80)
    print(f"RUNNING THRESHOLD = {threshold:.2f}")
    print("=" * 80)
    CONFIG.relationship_weight = 0.00
    CONFIG.premium_weight = 0.00

    CONFIG.conditional_premium_weight = 0.03

    CONFIG.conditional_spend_threshold = threshold

    CONFIG.name = (
        f"EXP003A_GATE_{threshold:.2f}"
    )

    result = main()

    results.append({

        "Threshold": threshold,
        "Weight": CONFIG.conditional_premium_weight,

        "Pearson": result["similarity"]["pearson"],
        "Spearman": result["similarity"]["spearman"],
        "Top20": result["similarity"]["top20_overlap"],

        "Spend": result["business"]["Spend"],
        "Revolve": result["business"]["Revolve"],
        "Risk": result["business"]["Risk"],
        "Profit": result["business"]["NetProfit"],
        "LTV": result["business"]["LTV"],

        "Decision": result["decision"],
    })

df = pd.DataFrame(results)

output = Path(
    "experiments/exp003a/results.csv"
)

output.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_csv(
    output,
    index=False,
)

print()
print("=" * 80)
print(df)