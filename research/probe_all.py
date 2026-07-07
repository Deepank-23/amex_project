"""
Probe Every Feature
"""

from __future__ import annotations

import pandas as pd

from src.config import CONFIG

from research.feature_probe import probe_feature


df = pd.read_csv(CONFIG.train_path)

if "id" in df.columns:
    df = df.rename(columns={"id": "ID"})


results = []

for feature in df.columns:

    if feature == "ID":
        continue

    try:

        result = probe_feature(feature)

        results.append(result)

    except Exception as e:

        print(feature, e)


results = pd.DataFrame(results)

results = results.sort_values(
    "Top20",
    ascending=False,
)

print()

print("=" * 80)
print("BEST FEATURES")
print("=" * 80)

print(results)

results.to_csv(
    "research/reports/feature_probe.csv",
    index=False,
)