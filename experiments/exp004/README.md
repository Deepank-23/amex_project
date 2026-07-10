# EXP004 Disagreement Clusters

## Business Hypothesis

Historical model disagreement contains information that average Top20 profiles hide.
Customers selected by exactly one strong historical philosophy (`BEST087`, `LTV079`,
or `NetProfit077`) may reveal the missing segment logic behind the hidden AMEX
objective.

## Reasoning

EXP001 through EXP003A showed that adding relationship, premium, conditional
premium, and thresholded premium signals barely moves the top set. Phase 2 should
therefore extract new evidence from historical submissions rather than add another
latent variable.

## Expected Outcome

This experiment should identify:

- `BEST_ONLY`, `LTV_ONLY`, and `PROFIT_ONLY` customer profiles.
- Pairwise disagreement segments between the three strongest historical models.
- Features most associated with rank disagreement between model philosophies.

## Implementation

Run:

```bash
python experiments/exp004/disagreement_clusters.py
```

Outputs:

- `experiments/exp004/results.csv`
- `research/reports/exp004/customer_disagreement_clusters.csv`
- `research/reports/exp004/cluster_feature_lifts.csv`
- `research/reports/exp004/pairwise_segment_summary.csv`
- `research/reports/exp004/rank_delta_correlations.csv`
