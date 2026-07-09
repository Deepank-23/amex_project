# Phase 2: Hidden Signal Discovery

## Objective

Rather than proposing experiments based on intuition, discover hidden business signals by analyzing how high-performing historical models rank customers.

The goal is to identify features that consistently characterize customers selected by successful models.

---

# Philosophy

Old Workflow

Idea
↓

Experiment
↓

Score

New Workflow

Evidence
↓

Hypothesis
↓

Experiment
↓

Offline Validation

Every experiment should begin with evidence from historical models.

---

# Research Questions

For every feature:

- Does this feature alone resemble successful models?
- Is this feature consistently elevated among top-ranked customers?
- Is the signal consistent across multiple successful submissions?
- Is the signal strong enough to justify a new experiment?

---

# Analysis Types

## 1. Feature Similarity Probe

Question:

"If I rank customers using only this feature, how similar is the ranking to the best historical model?"

Metrics

- Pearson
- Spearman
- Top20 Overlap

Purpose

Measure standalone predictive strength.

---

## 2. Consensus Feature Probe

Question

"Do successful models consistently prefer customers with high (or low) values of this feature?"

Procedure

Dataset Mean

↓

Top20 Mean for Best087

↓

Top20 Mean for LTV Model

↓

Top20 Mean for NetProfit Model

↓

Consensus Lift

Purpose

Measure business importance rather than predictive power.

---

## 3. Multi-Feature Consensus

Run the consensus probe across every unused feature.

Example

| Feature | Best087 | LTV | Profit | Consensus |
|----------|---------|-----|--------|-----------|
| Lounge | +46% | +45% | +44% | +45% |
| Login | +18% | +19% | +17% | +18% |
| Entertainment | +30% | +29% | +31% | +30% |

Purpose

Rank candidate features for future experiments.

---

# Expected Outcome

Instead of asking

"Should we try Lounge?"

the data should answer

"Lounge receives +45% lift across every successful historical model."

Only then should a new experiment be implemented.

---

# Success Criteria

A feature becomes an experiment candidate when

- Strong standalone signal

or

- Strong consensus lift across historical models

or

- Strong business intuition supported by consensus

---

# Deliverables

Research

- Feature Similarity Probe
- Consensus Feature Probe
- Multi-Feature Consensus Report

Experiments

- Engagement Score
- Interaction V2
- Relationship Refinement
- Issuer Economics Improvements

All future experiments should originate from evidence generated during this phase.