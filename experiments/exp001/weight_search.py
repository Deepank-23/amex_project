"""
EXP001 - Relationship Weight Search
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


WEIGHTS = [
    0.00,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
]

results = []


for weight in WEIGHTS:

    print("\n")
    print("=" * 80)
    print(f"RUNNING WEIGHT = {weight:.2f}")
    print("=" * 80)

    CONFIG.relationship_weight = 0.00

    CONFIG.name = f"EXP001_REL_{weight:.2f}"



    result = main()

    results.append({
        "Weight": weight,

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
    "experiments/exp001/results.csv"
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