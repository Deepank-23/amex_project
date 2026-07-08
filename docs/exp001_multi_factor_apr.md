# EXP001 — Multi-Factor APR

## Objective

Improve the issuer revenue model by replacing the current
risk-only APR assignment with a business-driven
multi-factor pricing function.

---

# Current Model

APR depends only on risk.

Risk Quartile

Q1 → 18%

Q2 → 22%

Q3 → 26%

Q4 → 29%

Interest Revenue

Interest =
Revolving Balance × APR × (1 − Risk)

---

# Problems

The current model assumes:

Two customers with identical risk always receive the same APR.

Real issuers do not price products this way.

Pricing also depends on:

- Customer behaviour
- Credit usage
- Relationship quality
- Expected profitability

---

# Candidate Variables

## 1. Risk (f11)

Reason

Primary determinant of pricing.

Expected Effect

Higher risk
↓

Higher APR

Confidence

★★★★★

---

## 2. Credit Utilization

Formula

f1 / f17

Reason

Customers using more of their credit line often generate
more revolving interest.

Expected Effect

Higher utilization
↓

Slightly higher APR

Confidence

★★★★☆

---

## 3. Revolving Balance

Reason

Large revolving balances create more interest revenue.

Question

Should APR increase with balance,
or is balance already captured in
Interest = Balance × APR?

Status

Needs investigation.

Confidence

★★★☆☆

---

## 4. Category Spend

Reason

High spend customers generate interchange revenue.

Question

Should banks reward these customers
with lower APR because they are already profitable?

Status

Open.

Confidence

★★☆☆☆

---

## 5. Engagement

Candidate

f12

Email

f22

Clicks

f23

Reason

Highly engaged customers are less likely to churn.

Possible Effect

Higher engagement

↓

Lower APR

Confidence

★★★☆☆

---

## 6. Benefit Usage

f13–f16

Reason

Heavy benefit users are costly.

Question

Should pricing compensate?

Status

Unknown.

Confidence

★★☆☆☆

---

## 7. Existing Credit

f17

f18

Reason

Large available credit reflects stronger relationship.

Possible Effect

Lower APR

Confidence

★★★☆☆

---

# Variables Excluded

Merchant revenue

Reason

Already modelled separately.

Reward breakage

Reason

Already modelled separately.

---

# Validation

Offline

✓ Component distributions

✓ Rank comparison

✓ Similarity vs baseline

✓ Customer movement

Leaderboard

Compare against baseline.

---

# Success Criteria

Higher leaderboard score than 0.87.

Otherwise reject.