# EXP001 - Relationship Score

## Status

COMPLETED

Decision: REVIEW (Not merged into baseline)

---

# Hypothesis

Customers with stronger long-term relationships with American Express should receive a higher ranking.

Relationship was modeled using:

- Supplementary Accounts (f19)
- Active Charge Cards (f20)
- Credit Line (f17)
- Consumer Credit Line (f18)

The relationship score was added as an additional component to the baseline model.

---

# Experiment

Relationship Weight Sweep

Weights Tested

- 0.00
- 0.01
- 0.02
- 0.03
- 0.04
- 0.05

Each configuration was evaluated using the offline validation framework.

---

# Results

| Weight | Spearman | Top20 | Spend | Profit | LTV |
|---------|-----------|--------|--------|---------|------|
|0.00|1.0000|1.0000|0.000|0.000|0.000|
|0.01|0.9995|0.9761|+0.134|-0.051|-0.085|
|0.02|0.9986|0.9523|+0.139|-0.110|-0.172|
|0.03|0.9972|0.9279|+0.188|-0.149|-0.242|
|0.04|0.9954|0.9029|+0.278|-0.207|-0.333|
|0.05|0.9932|0.8812|+0.349|-0.250|-0.412|

Observed behaviour

Increasing relationship weight:

✓ Increased Spend

✓ Increased Revolve Balance

✗ Increased Risk

✗ Reduced Net Profit

✗ Reduced LTV

The degradation was approximately monotonic across all tested weights.

---

# Conclusion

Relationship is a genuine customer characteristic.

However, adding relationship as an independent additive score does not improve the overall ranking.

The experiment suggests that relationship behaves more like a loyalty signal than a profitability signal.

---

# Key Insight

Relationship should probably not be modeled as

Final Score

=

Economics

+

Relationship

Instead, relationship is more likely to modify existing economics, for example:

Interest Revenue

=

Interest Revenue × Relationship Factor

or

Merchant Revenue

=

Merchant Revenue × Relationship Factor

This will be investigated in a future experiment.

---

# Outcome

Baseline remains unchanged.

Relationship feature is retained in the codebase but disabled by default.

No changes merged into the production baseline.

---

# Lessons Learned

- Offline validation framework successfully detected trade-offs.
- Weight search automation proved valuable.
- Relationship influences customer quality but is not a standalone ranking signal.
- Future experiments should focus on discovering new business signals rather than increasing relationship weight.
