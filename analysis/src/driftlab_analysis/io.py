"""Loading and validation for DriftLab task exports."""

import pandas as pd

# Must match shared/js/data-export.js REQUIRED_COLUMNS exactly — this is
# what lets any task's CSV load without task-specific code.
REQUIRED_COLUMNS = [
    "participant_id",
    "task",
    "block",
    "trial_index",
    "rt",
    "correct",
    "timestamp",
]


def load_csv(path):
    """Load a DriftLab task export CSV, validating the common schema.

    Raises ValueError listing the missing column(s) if the file doesn't
    have all the required columns.
    """
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"CSV at {path} is missing required column(s): {', '.join(missing)}. "
            f"Expected at least: {', '.join(REQUIRED_COLUMNS)}."
        )
    return df
