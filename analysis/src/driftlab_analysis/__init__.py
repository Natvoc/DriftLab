"""DriftLab analysis package: load, validate, and compute metrics for task
exports that follow the common data schema.
"""

from .io import load_csv
from .metrics import (
    MAX_VALID_RT_MS,
    MIN_VALID_RT_MS,
    accuracy,
    filter_valid_trials,
    mean_rt,
    stroop_effect,
)
from .simulate import simulate_stroop

__all__ = [
    "load_csv",
    "MIN_VALID_RT_MS",
    "MAX_VALID_RT_MS",
    "filter_valid_trials",
    "mean_rt",
    "accuracy",
    "stroop_effect",
    "simulate_stroop",
]
