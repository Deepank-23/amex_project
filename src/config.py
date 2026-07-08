"""
Project Configuration
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExperimentConfig:

    # --------------------------------------------------
    # Experiment
    # --------------------------------------------------

    baseline_mode: bool = True

    experiment_id: str = "EXP001"

    name: str = "EXP001_RELATIONSHIP"

    description: str = "Relationship Strength Feature"

    version: str = "1.0"

    # --------------------------------------------------
    # Data Paths
    # --------------------------------------------------

    data_dir: Path = Path("data")

    train_path: Path = data_dir / "dataset.csv"

    # --------------------------------------------------
    # Output Paths
    # --------------------------------------------------

    output_dir: Path = Path("outputs")

    submission_dir: Path = output_dir / "submissions"

    raw_score_dir: Path = output_dir / "raw_scores"

    report_dir: Path = output_dir / "reports"

    # --------------------------------------------------
    # APR
    # --------------------------------------------------

    apr_low: float = 0.18
    apr_mid1: float = 0.22
    apr_mid2: float = 0.26
    apr_high: float = 0.29

    # --------------------------------------------------
    # Economics
    # --------------------------------------------------

    interchange_rate: float = 0.02

    breakage_value: float = 0.0075

    # --------------------------------------------------
    # Model Weights
    # --------------------------------------------------

    interest_weight: float = 0.374

    merchant_weight: float = 0.501

    breakage_weight: float = 0.125

    interaction_weight: float = 0.200

    risk_weight: float = 0.050

    # --------------------------------------------------
    # Experiment Flags
    # --------------------------------------------------

    use_relationship_score: bool = True

    relationship_weight: float = 0.05

    relationship_weights = {
        "supplementary": 0.35,
        "charge_cards": 0.35,
        "credit_line": 0.15,
        "consumer_credit": 0.15,
    }

    # --------------------------------------------------
    # Automatic File Paths
    # --------------------------------------------------

    @property
    def submission_path(self) -> Path:
        return self.submission_dir / f"{self.name}.csv"

    @property
    def raw_score_path(self) -> Path:
        return self.raw_score_dir / f"{self.name}_SCORE.csv"

    @property
    def report_path(self) -> Path:
        return self.report_dir / self.name


CONFIG = ExperimentConfig()