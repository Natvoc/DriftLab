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
