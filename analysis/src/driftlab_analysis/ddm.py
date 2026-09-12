"""Drift-diffusion model fitting via PyDDM.

Not imported by driftlab_analysis/__init__.py on purpose: pyddm is an
opt-in dependency (see DECISIONS.md, 2026-08-25 — it only imports inside
WSL2 on this project's dev machine, not the Windows venv), so importing
`driftlab_analysis` itself must keep working without pyddm installed.
Import this submodule explicitly when you need DDM fitting:

    from driftlab_analysis.ddm import fit_ddm_by_condition
"""

import pyddm

from .metrics import filter_valid_trials

RT_MS_PER_S = 1000  # PyDDM expects RT in seconds; our schema stores ms

# Search bounds for the fitted parameters. Wide enough to cover plausible
# Stroop-like RT distributions without being so wide the optimizer wastes
# time in implausible regions.
DRIFT_FIT_MIN = 0.0
DRIFT_FIT_MAX = 5.0
BOUND_FIT_MIN = 0.2
BOUND_FIT_MAX = 3.0
NONDECISION_FIT_MIN = 0.0
NONDECISION_FIT_MAX = 1.0
T_DUR_S = 3.0  # max decision time considered by the model, in seconds


def _build_sample(df):
    df = df.copy()
    df["rt_seconds"] = df["rt"] / RT_MS_PER_S
    return pyddm.Sample.from_pandas_dataframe(
        df,
        rt_column_name="rt_seconds",
        choice_column_name="correct",
        choice_names=("correct", "error"),
    )


def fit_ddm(df, seed=None):
    """Fit a simple DDM (drift rate, threshold, non-decision time free;
    noise fixed at 1, the standard PyDDM convention) to one condition's
    worth of trials.

    df: DataFrame in the common schema (rt in ms, correct 0/1). Invalid
    trials (see metrics.filter_valid_trials) are dropped before fitting.
    seed: optional seed for the differential-evolution optimizer, for
    reproducible fits (used by the parameter-recovery test; leave as None
    for real use, where exact reproducibility of the optimizer path isn't
    the point).

    Returns {"drift_rate": float, "threshold": float,
    "non_decision_time": float (seconds)}.
    """
    valid = filter_valid_trials(df)
    sample = _build_sample(valid)

    model = pyddm.gddm(
        drift=pyddm.Fittable(minval=DRIFT_FIT_MIN, maxval=DRIFT_FIT_MAX),
        noise=1,
        bound=pyddm.Fittable(minval=BOUND_FIT_MIN, maxval=BOUND_FIT_MAX),
        nondecision=pyddm.Fittable(minval=NONDECISION_FIT_MIN, maxval=NONDECISION_FIT_MAX),
        T_dur=T_DUR_S,
    )
    fitparams = {"seed": seed} if seed is not None else None
    model.fit(sample, verbose=False, fitparams=fitparams)

    # PyDDM's internal parameter names ("B", "nondectime") don't match the
    # gddm() kwargs used to define them ("bound", "nondecision") — mapped
    # here once, discovered via introspection (see DECISIONS.md, 2026-08-25).
    fitted = dict(zip(model.get_model_parameter_names(), model.get_model_parameters()))
    return {
        "drift_rate": float(fitted["drift"]),
        "threshold": float(fitted["B"]),
        "non_decision_time": float(fitted["nondectime"]),
    }


def fit_ddm_by_condition(df, condition_col="congruency", seed=None):
    """Fit a DDM separately for each value of `condition_col`.

    Returns {condition_value: {"drift_rate", "threshold",
    "non_decision_time"}}. Reusable as-is for real data — just pass a
    DataFrame loaded via driftlab_analysis.io.load_csv.
    """
    return {
        condition: fit_ddm(group, seed=seed) for condition, group in df.groupby(condition_col)
    }
