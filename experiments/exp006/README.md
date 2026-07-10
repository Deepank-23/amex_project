# EXP006 Prototype Router

## Business Hypothesis

The hidden objective rewards customers who resemble the strongest shared
historical archetypes, not customers who optimize a single business philosophy.

## Reasoning

EXP004 showed that:

- `ALL_THREE` is the strongest and most balanced customer cluster.
- `BEST_LTV` looks like a valuable secondary pattern.
- `LTV_ONLY` and `PROFIT_ONLY` are the two clearest failure modes.

Instead of adding one more scalar business term, this experiment measures
customer similarity to good prototypes and dissimilarity from bad prototypes.

## Expected Outcome

This experiment should produce a more expressive ranking than a flat linear
score because it can explicitly separate balanced, high-value customers from
one-sided extremes.

## Implementation

Run:

```bash
python experiments/exp006/prototype_router_search.py
```

Outputs:

- `experiments/exp006/results.csv`
- `outputs/raw_scores/EXP006_PROTOTYPE_ROUTER_SCORE.csv`
- `outputs/submissions/EXP006_PROTOTYPE_ROUTER.csv`
