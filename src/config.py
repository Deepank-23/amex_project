from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

OUTPUT_DIR = ROOT_DIR / "outputs"

TRAIN_PATH = DATA_DIR / "dataset.csv"

FEATURE_PATH = DATA_DIR / "features.csv"

SUBMISSION_PATH = DATA_DIR / "sample_submission.xlsx"