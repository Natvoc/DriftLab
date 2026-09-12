"""Loading and validation for DriftLab task exports."""

import pandas as pd

# Must match shared/js/data-export.js REQUIRED_COLUMNS exactly — this is
# what lets any task's export load without task-specific code.
REQUIRED_COLUMNS = [
    "participant_id",
    "task",
    "block",
    "trial_index",
    "rt",
    "correct",
    "timestamp",
]


def _validate_schema(df, path):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"File at {path} is missing required column(s): {', '.join(missing)}. "
            f"Expected at least: {', '.join(REQUIRED_COLUMNS)}."
        )
    return df


def load_csv(path):
    """Load a DriftLab task export CSV, validating the common schema.

    Raises ValueError listing the missing column(s) if the file doesn't
    have all the required columns.
    """
    return _validate_schema(pd.read_csv(path), path)


def load_json(path):
    """Load a DriftLab task export JSON (the other format data-export.js
    can produce, alongside CSV), validating the common schema the same
    way load_csv does.
    """
    return _validate_schema(pd.read_json(path), path)


def load_export(path):
    """Load a DriftLab task export, dispatching to load_csv or load_json
    based on the file extension."""
    path_str = str(path)
    if path_str.endswith(".json"):
        return load_json(path)
    if path_str.endswith(".csv"):
        return load_csv(path)
    raise ValueError(f"Don't know how to load {path}: expected a .csv or .json file.")
