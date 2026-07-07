"""
Project Configuration
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExperimentConfig:
    baseline_mode: bool = True
    # ----------------------------
    # Experiment Info
    # ----------------------------
    name: str = "BEST_087"
    description: str = "Reproduce best public model"

    # ----------------------------
    # Data Paths
    # ----------------------------
    data_dir: Path = Path("data")
    train_path: Path = Path("data") / "dataset.csv"
    submission_dir: Path = Path("outputs") / "submissions"

    # ----------------------------
    # APR
    # ----------------------------
    apr_low: float = 0.18
    apr_mid1: float = 0.22
    apr_mid2: float = 0.26
    apr_high: float = 0.29

    # ----------------------------
    # Economics
    # ----------------------------
    interchange_rate: float = 0.02
    breakage_value: float = 0.0075

    # ----------------------------
    # Weights
    # ----------------------------
    interest_weight: float = 0.374
    merchant_weight: float = 0.501
    breakage_weight: float = 0.125
    interaction_weight: float = 0.200
    risk_weight: float = 0.050


CONFIG = ExperimentConfig()