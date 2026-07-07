from submission_loader import load_submissions
from overlap import compare_submissions

subs = load_submissions()

compare_submissions(
    subs["AMEX_R1_BEST_087"],
    subs["AMEX_R1_LTV_Model_079"],
    "BEST",
    "LTV",
)