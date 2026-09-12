"""Synthetic Stroop data generation, so tests and the demo notebook have
something deterministic to run against without anyone having to play the
task first.
"""

import numpy as np
import pandas as pd

COLORS = ["red", "green", "blue", "yellow"]

CONGRUENT_MEAN_RT = 650
INCONGRUENT_MEAN_RT = 750
RT_SD = 120
ACCURACY_RATE = 0.95


def simulate_stroop(n_trials_per_condition=24, seed=42):
    """Generate a synthetic Stroop test-block dataset in the common
    schema, with the classic effect (incongruent slower than congruent)
    built in. Reproducible for a given seed.
    """
    rng = np.random.default_rng(seed=seed)
    participant_id = f"sim-{seed:08d}"
    base_time = pd.Timestamp("2026-01-01T00:00:00Z")

    specs = [("congruent", CONGRUENT_MEAN_RT)] * n_trials_per_condition + [
        ("incongruent", INCONGRUENT_MEAN_RT)
    ] * n_trials_per_condition
    order = rng.permutation(len(specs))

    rows = []
    for trial_index, spec_i in enumerate(order):
        congruency, mean_rt_ms = specs[spec_i]
        word = COLORS[rng.integers(0, len(COLORS))]
        if congruency == "congruent":
            ink_color = word
        else:
            ink_color = rng.choice([c for c in COLORS if c != word])
        rt = max(150.0, float(rng.normal(mean_rt_ms, RT_SD)))
        correct = 1 if rng.random() < ACCURACY_RATE else 0

        rows.append(
            {
                "participant_id": participant_id,
                "task": "stroop",
                "block": "test",
                "trial_index": trial_index,
                "rt": round(rt, 1),
                "correct": correct,
                "timestamp": (base_time + pd.Timedelta(seconds=3 * trial_index)).isoformat(),
                "word": word.upper(),
                "ink_color": ink_color,
                "congruency": congruency,
            }
        )

    return pd.DataFrame(rows)


# "True" generative parameters for the DDM toy dataset below. Drift rate
# differs by condition (the effect we want the fit to recover); bound is
# identical across conditions ON PURPOSE, so a parameter recovery check can
# confirm the fit attributes the effect to drift rate and not to a spurious
# threshold difference. Units: drift/bound in PyDDM's internal scale,
# non-decision time in seconds (PyDDM works in seconds, not ms).
DDM_TOY_DRIFT_CONGRUENT = 2.0
DDM_TOY_DRIFT_INCONGRUENT = 1.2
DDM_TOY_BOUND = 1.0
DDM_TOY_NONDECISION_S = 0.3
DDM_TOY_T_DUR_S = 3.0
# ~150-200+ trials/condition is the threshold noted in DECISIONS.md
# (2026-08-25) for a real fit not to come out noisy; used as the default
# here too so the toy check is representative of what a real fit will face.
DDM_TOY_N_TRIALS_PER_CONDITION = 200


def simulate_stroop_ddm_toy(n_trials_per_condition=DDM_TOY_N_TRIALS_PER_CONDITION, seed=42):
    """Generate a synthetic 2-condition (congruent/incongruent) dataset by
    actually sampling from a DDM with known ("true") parameters, for
    validating that the PyDDM fitting pipeline recovers them (parameter
    recovery) — this is a toy/validation dataset, NOT a stand-in for real
    Stroop data (see simulate_stroop for that). `task` is set to
    "stroop_ddm_toy" specifically so it can't be confused with real or
    metrics-oriented synthetic data downstream.

    Returns a DataFrame in the common schema (rt in ms, per shared/js/
    data-export.js) plus a `congruency` column.
    """
    import pyddm  # local import: keeps `pyddm` an opt-in dependency for

    # only the DDM-fitting path, not for the whole driftlab_analysis package
    # (see DECISIONS.md, 2026-08-25 — pyddm doesn't import on the Windows
    # venv on this project's dev machine, only inside WSL2).

    rng = np.random.default_rng(seed=seed)
    participant_id = f"ddm-toy-{seed:08d}"
    base_time = pd.Timestamp("2026-01-01T00:00:00Z")

    condition_drifts = [
        ("congruent", DDM_TOY_DRIFT_CONGRUENT),
        ("incongruent", DDM_TOY_DRIFT_INCONGRUENT),
    ]

    rows = []
    trial_index = 0
    for congruency, drift in condition_drifts:
        model = pyddm.gddm(
            drift=drift,
            noise=1,
            bound=DDM_TOY_BOUND,
            nondecision=DDM_TOY_NONDECISION_S,
            T_dur=DDM_TOY_T_DUR_S,
        )
        sample = model.solve().sample(
            k=n_trials_per_condition, seed=int(rng.integers(0, 2**31 - 1))
        )
        sample_df = sample.to_pandas_dataframe()  # columns: choice (1/0), RT (seconds)

        for _, trial in sample_df.iterrows():
            rows.append(
                {
                    "participant_id": participant_id,
                    "task": "stroop_ddm_toy",
                    "block": "test",
                    "trial_index": trial_index,
                    "rt": round(float(trial["RT"]) * 1000, 1),
                    "correct": int(trial["choice"]),
                    "timestamp": (base_time + pd.Timedelta(seconds=3 * trial_index)).isoformat(),
                    "congruency": congruency,
                }
            )
            trial_index += 1

    return pd.DataFrame(rows)
