# 📂 Module Responsibilities (Frozen)

## offline_validation.py
- Orchestrates the validation process
- Prints section headers
- Calls each module
- Passes results to the recommendation engine

---

## similarity.py
- Pearson correlation
- Spearman correlation
- MAE (Mean Absolute Error)
- Median AE
- Max Difference
- Top‑20 Overlap (if implemented here)

---

## customer_difference.py
- Rank changes
- Largest promotions
- Largest demotions
- Entered Top‑20
- Exited Top‑20
- Save customer movement CSV

---

## business_metrics.py
- Compare Baseline Top‑20 vs Experiment Top‑20
- Metrics:
  - Net Profit
  - LTV (Lifetime