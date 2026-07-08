# AMEX Campus Challenge R1
## Experiment Backlog

---

# Current Status

## Baseline

Status: ✅ Reproduced

Leaderboard:
0.87

Validation:
Pearson = 1.000000
Spearman = 1.000000

Do NOT modify baseline files.

---

# Completed Experiments

| ID | Experiment | Result | Status | Notes |
|----|------------|--------|--------|-------|
| BASE | Original BEST model | 0.87 | ✅ Locked | Exact reproduction completed |
| OLD-ENS | Simple Ensemble | Worse than baseline | ❌ Rejected | Already tested previously. Do not repeat unless using a fundamentally different ensemble method. |

---

# High Priority

##EXP001A- reltionship factor

BASELINE VALIDATION
================================================================================

Rows
Current    : 500000
Historical : 500000
Merged     : 500000


================================================================================
CORRELATION
================================================================================
Pearson  : 0.99823115
Spearman : 0.99319626


================================================================================
ERROR
================================================================================
Mean Absolute Error : 0.045815389534259045
Median Absolute Error : 0.04634157200519301
Maximum Difference : 0.11447485961172155

## EXP001 — Weight Optimization

Priority: ⭐⭐⭐⭐⭐

Goal:
Optimize the existing component weights while keeping the model structure unchanged.

Current:

Interest = 0.374
Merchant = 0.501
Breakage = 0.125
Interaction = 0.200
Risk = 0.050

Expected Gain:
Medium–High

Difficulty:
Medium

Status:
Not Started

---

## EXP002 — Multi-Factor Revenue Rate

Priority: ⭐⭐⭐⭐⭐

Goal:
Replace the single-factor APR (based only on f11) with a revenue-rate model that incorporates additional customer characteristics.

Candidate Inputs:

- f11 (risk)
- utilization (f1 / f17)
- spend
- engagement
- servicing cost

Expected Gain:
High

Difficulty:
Medium

Status:
Not Started

---

## EXP003 — Interaction Features v2

Priority: ⭐⭐⭐⭐☆

Goal:
Replace the current interaction term with more expressive alternatives.

Ideas:

- Geometric mean
- Harmonic mean
- Rank product
- Weighted interaction
- Conditional interaction

Status:
Not Started

---

## EXP004 — Customer Segmentation

Priority: ⭐⭐⭐⭐☆

Goal:
Create different profitability models for different customer segments.

Examples:

- High spenders
- High revolvers
- Low-risk customers
- Rewards-heavy customers

Status:
Not Started

---

## EXP005 — Feature Discovery

Priority: ⭐⭐⭐⭐☆

Goal:
Use the research framework to identify new engineered features.

Status:
Not Started

---

## EXP006 — Learning-to-Rank

Priority: ⭐⭐⭐☆☆

Goal:
Use the business score as supervision for a ranking model.

Status:
Future Work

---

# Rejected Ideas

| Idea | Reason |
|------|--------|
| Simple rank averaging | Reduced leaderboard score |
| Simple ensemble | Reduced leaderboard score |

---

# Rules

1. One experiment = one hypothesis.
2. Never modify the locked baseline.
3. Record every result.
4. Do not repeat rejected ideas unless the implementation is fundamentally different.
5. Every accepted experiment must outperform the current baseline.

# Research Questions

1. Why does the BEST model outperform LTV by ~0.08?
2. Which customers contribute most to the leaderboard gain?
3. Which business assumptions are unsupported?
4. Which engineered features have never been tested?
5. Which experiments can be evaluated offline?