# EXP005 Segment Router

## Business Hypothesis

The hidden objective is not a single business philosophy. It rewards customers
who are strong on both spend and revolve, while penalizing one-sided extremes:

- safe, benefit-heavy customers with weak revolve
- risky, revolve-heavy customers with weak spend

## Reasoning

EXP004 showed:

- `ALL_THREE` customers are strong on both spend and revolve.
- `LTV_ONLY` customers are retention-heavy but weak on revolve.
- `PROFIT_ONLY` customers are revolve-heavy but weak on spend and riskier.

That means the next model should route by customer style rather than keep adding
flat additive features.

## Expected Outcome

This experiment should produce a score that:

- keeps the strong `BEST087` core,
- boosts balanced dual-value customers,
- penalizes the two disagreement failure modes,
- stays close enough to historical winners to remain plausible.

## Implementation

Run:

```bash
python experiments/exp005/segment_router_search.py
```

Outputs:

- `experiments/exp005/results.csv`
- `outputs/raw_scores/EXP005_SEGMENT_ROUTER_SCORE.csv`
- `outputs/submissions/EXP005_SEGMENT_ROUTER.csv`
