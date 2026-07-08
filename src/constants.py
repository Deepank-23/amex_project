LOG_FEATURES = [
    "f1",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
]

RANK_FEATURES = [
    "f1",
    "f5",
]
WEIGHTS = {
    "interest": 0.374,
    "merchant": 0.501,
    "breakage": 0.125,
    "interaction": 0.200,
    "risk": 0.050,

    # EXP001
    "relationship": 0.050,
}
BINARY_FEATURES = []

MISSING_THRESHOLD = 0.10

LOWER_CLIP = 0.01

UPPER_CLIP = 0.99

EPSILON = 1e-9

TOP_PERCENT = 0.20

BASELINE_SCORE = 20.0

RANDOM_STATE = 42