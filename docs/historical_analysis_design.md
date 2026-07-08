# Historical Analysis Engine
Version: 1.0
Status: Planned (Phase 2)
Not implemented till now
---

# Objective

Learn from every previous submission and every future experiment to identify
consistent business signals that improve ranking.

Rather than evaluating a single experiment against the baseline, this engine
analyzes the evolution of customer rankings across multiple models and tests
whether each experiment's hypothesis is supported by evidence.

---

# Goals

1. Track how every customer's rank changes across model versions.
2. Discover which customer characteristics consistently lead to promotion.
3. Validate or reject historical hypotheses.
4. Identify stable high-value customers.
5. Build evidence before creating new experiments.

---

# Inputs

## Dataset

data/dataset.csv

---

## Submission Files

All historical submissions.

Examples

AMEX_R1_BEST_087

AMEX_R1_LTV_Model_079

AMEX_R1_NetProfit_Model_077

submission_026

submission_049

submission_053

submission_063

submission_066

submission_067

Future experiments

EXP001

EXP002

...

---

## Experiment Metadata

Each submission should contain metadata.

Example

| Submission | Hypothesis |
|------------|------------|
|026|Baseline|
|049|Spend emphasis|
|053|Interaction weighting|
|063|Merchant optimization|
|066|Ensemble|
|067|Category spend|
|077|Net Profit optimization|
|079|LTV optimization|
|087|Balanced business model|
|EXP001|Relationship strength|
|EXP002|Continuous APR|

---

# Core Analyses

## 1. Customer Journey

Track rank over time.

Output

ID

Rank in every submission

Promotion trend

Demotion trend

Stable rank

Example

ID

026

049

053

063

066

067

077

079

087

EXP001

...

---

## 2. Promotion Frequency

For every customer

Count

Times promoted

Times demoted

Average rank

Maximum promotion

Maximum demotion

Promotion stability score

---

## 3. Top20 Stability

Questions

How many customers always stay in Top20?

Who repeatedly enters?

Who repeatedly exits?

Who oscillates?

Output

Stable Elite

Emerging Customers

Declining Customers

Volatile Customers

---

## 4. Feature Evolution

For promoted customers

Compare

Spend

Risk

Credit Line

Relationship

Rewards

Emails

Supplementary Cards

Charge Cards

LTV

Net Profit

Determine which features consistently improve.

---

## 5. Consensus Analysis

Consensus score

How many models ranked a customer highly?

Example

Customer

Top20 Frequency

026

049

053

063

066

067

077

079

087

Consensus Score

---

## 6. Hypothesis Validation

Every experiment has a business hypothesis.

Examples

Relationship matters.

Higher spend customers should rank higher.

Low-risk customers deserve higher APR.

LTV is a stronger indicator than Net Profit.

Question

Did the experiment actually promote customers matching the hypothesis?

Decision

SUPPORTED

PARTIALLY SUPPORTED

REJECTED

---

## 7. Feature Importance by Observation

Without training ML models.

Use observed promotions.

Example

Promoted customers

Average Supplementary Accounts

Average Charge Cards

Average Spend

Average Risk

Average Credit Line

Compare with demoted customers.

Repeat across every submission.

Identify consistently changing features.

---

## 8. Experiment Similarity

Compare every pair of submissions.

Already available

Pearson

Spearman

Top20 Overlap

Extend later

Customer movement similarity

Hypothesis similarity

---

## 9. Experiment Timeline

Chronological evolution.

026

↓

049

↓

053

↓

063

↓

066

↓

067

↓

077

↓

079

↓

087

↓

EXP001

↓

EXP002

...

Understand why each iteration improved or deteriorated.

---

# Expected Outputs

Customer Journey Report

Promotion Frequency Report

Feature Evolution Report

Hypothesis Validation Report

Consensus Rankings

Experiment Similarity Matrix

Historical Summary

---

# Future Visualizations

Customer rank trajectories

Promotion heatmaps

Feature evolution charts

Consensus graphs

Experiment network graph

---

# Success Criteria

The engine should answer:

Why did customers move?

Which business features consistently matter?

Which hypotheses were successful?

Which hypotheses repeatedly failed?

Which customers are consistently valuable?

What should be tested next?

---

# Phase

Not part of the production pipeline.

Runs only after experiments.

Workflow

Experiment

↓

Offline Validator

↓

Decision

↓

Historical Analysis Engine

↓

Next Experiment Design

---

# Notes

This engine is intended to guide future experiments, not generate submissions.

It serves as a research knowledge base and evidence framework built from every historical submission and every experiment performed in this repository.