"""Parameter recovery test for the PyDDM fitting pipeline.

Not skipped by default: a full fit over both conditions takes ~2s locally
(measured 2026-08-25), so there's no runtime reason to opt it out of the
normal test run. Uses a fixed optimizer seed so the recovered values are
reproducible instead of merely "close on average" (see ddm.fit_ddm's
`seed` param, added for this test).
"""

from driftlab_analysis.ddm import fit_ddm_by_condition
from driftlab_analysis.simulate import (
    DDM_TOY_BOUND,
    DDM_TOY_DRIFT_CONGRUENT,
    DDM_TOY_DRIFT_INCONGRUENT,
    DDM_TOY_NONDECISION_S,
    simulate_stroop_ddm_toy,
)

# Generous but meaningful tolerances: loose enough to absorb the sampling
# noise inherent to a ~200-trials-per-condition fit, tight enough that a
# genuinely broken pipeline (wrong RT units, swapped parameters, a bad
# PyDDM API mapping) would still fail this.
DRIFT_TOLERANCE = 0.7
THRESHOLD_TOLERANCE = 0.4
NONDECISION_TOLERANCE_S = 0.15

FIT_SEED = 123


def test_ddm_parameter_recovery_on_synthetic_data():
    df = simulate_stroop_ddm_toy()
    fitted = fit_ddm_by_condition(df, seed=FIT_SEED)

    congruent = fitted["congruent"]
    incongruent = fitted["incongruent"]

    assert abs(congruent["drift_rate"] - DDM_TOY_DRIFT_CONGRUENT) < DRIFT_TOLERANCE
    assert abs(incongruent["drift_rate"] - DDM_TOY_DRIFT_INCONGRUENT) < DRIFT_TOLERANCE

    for condition in (congruent, incongruent):
        assert abs(condition["threshold"] - DDM_TOY_BOUND) < THRESHOLD_TOLERANCE
        assert (
            abs(condition["non_decision_time"] - DDM_TOY_NONDECISION_S)
            < NONDECISION_TOLERANCE_S
        )

    # The actual scientific claim being validated: the fit attributes the
    # simulated Stroop-like effect to drift rate, not to threshold — this
    # is the whole point of the toy dataset (same bound, different drift).
    assert congruent["drift_rate"] > incongruent["drift_rate"]
