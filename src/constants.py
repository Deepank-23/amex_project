"""
Project Constants
"""

# -------------------------------
# Feature Groups
# -------------------------------

LOG_FEATURES = [
    "f1", "f4", "f5", "f6", "f7",
    "f8", "f9", "f10", "f17",
    "f18", "f21"
]

RANK_FEATURES = [
    "f1", "f4", "f5", "f6", "f7",
    "f8", "f9", "f10", "f11",
    "f12", "f17", "f18",
    "f21", "f22", "f23"
]

BINARY_FEATURES = [
    "f2",
    "f3",
    "f20"
]

# -------------------------------
# Preprocessing
# -------------------------------

MISSING_THRESHOLD = 0.05

LOWER_CLIP = 0.005

UPPER_CLIP = 0.995

EPSILON = 1e-6