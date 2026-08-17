import pandas as pd
import pytest

from driftlab_analysis import load_csv, simulate_stroop, stroop_effect


def test_stroop_effect_has_expected_sign_on_synthetic_data():
    df = simulate_stroop(n_trials_per_condition=100, seed=42)
    assert stroop_effect(df) > 0


def test_load_csv_raises_clear_error_on_missing_columns(tmp_path):
    csv_path = tmp_path / "bad_export.csv"
    pd.DataFrame({"participant_id": ["p1"], "task": ["stroop"]}).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="missing required column"):
        load_csv(csv_path)
