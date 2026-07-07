"""
Utility Functions
"""

from __future__ import annotations

import json
import os

from dataclasses import asdict

from src.config import CONFIG


def save_experiment_metadata():

    os.makedirs(
        "experiments",
        exist_ok=True,
    )

    with open(
        "experiments/current_config.json",
        "w",
    ) as f:

        json.dump(
            asdict(CONFIG),
            f,
            indent=4,
        )