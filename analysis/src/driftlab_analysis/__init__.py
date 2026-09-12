"""DriftLab analysis package: load, validate, and compute metrics for task
exports that follow the common data schema.
"""

from .data_quality import check_trial_counts, count_valid_trials
from .io import load_csv
from .metrics import (
    MAX_VALID_RT_MS,
    MIN_VALID_RT_MS,
    accuracy,
    filter_valid_trials,
    mean_rt,
    stroop_effect,
)
from .simulate import simulate_stroop, simulate_stroop_ddm_toy

# NOTE: driftlab_analysis.ddm is deliberately NOT imported here — it
# imports pyddm at module level, which is an opt-in dependency (see
# DECISIONS.md, 2026-08-25). Import it explicitly when needed:
#   from driftlab_analysis.ddm import fit_ddm_by_condition

__all__ = [
    "load_csv",
    "MIN_VALID_RT_MS",
    "MAX_VALID_RT_MS",
    "filter_valid_trials",
    "mean_rt",
    "accuracy",
    "stroop_effect",
    "simulate_stroop",
    "simulate_stroop_ddm_toy",
    "count_valid_trials",
    "check_trial_counts",
]
