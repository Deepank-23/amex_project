"""
Project Configuration
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=False)
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
    submission_template_path: Path = (
        data_dir / "6a3cb64c7cae4_campus_challenge_r1_submission_template.xlsx"
    )

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

    breakage_weight: float = 0.085

    interaction_weight: float = 0.140

    risk_weight: float = 0.150

    # --------------------------------------------------
    # Experiment Flags
    # --------------------------------------------------

    use_relationship_score: bool = False

    relationship_weight: float =0

    relationship_weights = {
        "supplementary": 0.35,
        "charge_cards": 0.35,
        "credit_line": 0.15,
        "consumer_credit": 0.15,
    }

    # ----------------------------
    # Premium Engagement
    # ----------------------------

    use_premium_score: bool = False

    premium_weight: float = 0.03
    lounge_weight = 0.20          # f13
    airline_weight = 0.30         # f14
    cab_weight = 0.10             # f15
    entertainment_weight = 0.25   # f16
    email_open_weight = 0.10      # f22
    email_click_weight = 0.05     # f23
    # --------------------------------------------------
    # Automatic File Paths
    # --------------------------------------------------
    # ----------------------------
    # Conditional Premium
    # ----------------------------

    use_conditional_premium: bool = False
    conditional_spend_threshold: float = 0.50

    conditional_premium_weight: float = 0.03
    @property
    def submission_path(self) -> Path:
        return self.submission_dir / f"{self.name}.csv"

    @property
    def submission_workbook_path(self) -> Path:
        return self.submission_dir / f"{self.name}.xlsx"

    @property
    def raw_score_path(self) -> Path:
        return self.raw_score_dir / f"{self.name}_SCORE.csv"

    @property
    def report_path(self) -> Path:
        return self.report_dir / self.name


CONFIG = ExperimentConfig()
