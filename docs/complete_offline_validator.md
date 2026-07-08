# 📑 Offline Validation Framework

## 1. Pipeline Health ✅
- **Checks:**
  - PASS / FAIL
  - Row counts
  - NaNs
  - Inf values
  - Duplicate IDs
  - Rank ties

---

## 2. Submission Similarity
- Already implemented.
- Metrics:
  - Pearson correlation
  - Spearman correlation
  - MAE (Mean Absolute Error)
  - Top‑20 overlap

---

## 3. Customer Movement ⭐⭐⭐
- **Missing, needs implementation.**
- Metrics:
  - Top‑20 Added
  - Top‑20 Removed
  - Largest Promotions
  - Largest Demotions
  - Average Rank Change
  - Median Rank Change

---

## 4. Business Comparison ⭐⭐⭐⭐⭐
- Compare **Top‑20 Baseline vs. Top‑20 Experiment**.
- Proxy labels:
  - Average Revolve Balance
  - Average Spend
  - Average Risk
  - Average Interest Revenue
  - Average Merchant Revenue
  - Average Net Profit
  - Average LTV

---

## 5. Feature Comparison ⭐⭐⭐⭐⭐
- Automatically compare all features (`f1 … f23`).
- Focus on:
  - Relationship
  - Utilization
  - Category Spend
- Sort by **absolute difference**.
- Report:
  - Top 10 Increased
  - Top 10 Decreased

---

## 6. Promoted Customer Profile ⭐⭐⭐⭐⭐
- For customers entering the Top‑20:
  - Average Spend
  - Average Risk
  - Average Supplementary Accounts
  - Average Charge Cards
  - Average Login
  - Average Email Opens
  - Average Credit Line

---

## 7. Demoted Customer Profile
- Same metrics as promoted customers.
- Explains **why the model swapped them**.

---

## 8. Component Comparison ⭐⭐⭐
- Business model components (Top‑20 only):
  - Interest
  - Merchant
  - Breakage
  - Interaction
  - Relationship
  - Risk

---

## 9. Score Distribution
- Metrics:
  - Mean
  - Std (Standard Deviation)
  - Percentiles
  - Histogram (optional)

---

## 10. Recommendation ⭐⭐⭐⭐⭐
- **Rule‑based, not AI.**
- Example rule:
  - If **Similarity > 0.98**
  - AND **Spend increases**
  - AND **Net Profit increases**
  - AND **Risk does not increase**
  - → **PROMISING**
- Otherwise:
  - REJECT
  - or REVIEW

---

# 🛠️ Validator Script Structure (`offline_validation.py`)

```plaintext
offline_validation.py
│
├── validate_pipeline()
├── compare_similarity()
├── analyze_customer_movement()
├── compare_business_metrics()
├── compare_features()
├── compare_components()
├── generate_recommendation()
└── export_report()

outputs/
    reports/
        exp001/
            summary.txt
            customer_changes.csv
            promoted_customers.csv
            demoted_customers.csv
            feature_changes.csv
            business_metrics.csv
            recommendation.json


flowchart TD
    A[validate_pipeline] --> B[compare_similarity]
    B --> C[analyze_customer_movement]
    C --> D[compare_business_metrics]
    D --> E[compare_features]
    E --> F[compare_components]
    F --> G[generate_recommendation]
    G --> H[export_report]
