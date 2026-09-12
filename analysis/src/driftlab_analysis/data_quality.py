"""Quick "do I have enough data yet?" check for real task exports.

Run as a script against a real CSV in analysis/data/raw/ once real data
exists, to check trial counts before requesting/running a real DDM fit:

    python -m driftlab_analysis.data_quality path/to/export.csv
"""

import sys

from .io import load_csv
from .metrics import filter_valid_trials

# Low end of the ~150-200+ trials/condition/participant range noted in
# DECISIONS.md (2026-08-25) as what a DDM fit needs to not come out noisy.
MIN_TRIALS_PER_CONDITION = 150


def count_valid_trials(df, condition_col="congruency"):
    """Count valid trials per participant and condition.

    Returns a DataFrame indexed by (participant_id, condition_col) with a
    single `n_valid_trials` column.
    """
    valid = filter_valid_trials(df)
    counts = valid.groupby(["participant_id", condition_col]).size()
    return counts.rename("n_valid_trials").to_frame()


def check_trial_counts(df, condition_col="congruency", min_trials=MIN_TRIALS_PER_CONDITION):
    """Print a per-participant/condition trial count report and flag any
    cell below `min_trials`.

    Returns True if every participant/condition combination has at least
    `min_trials` valid trials, False otherwise.
    """
    counts = count_valid_trials(df, condition_col=condition_col)

    print(counts.to_string())
    print()

    below_threshold = counts[counts["n_valid_trials"] < min_trials]
    if below_threshold.empty:
        print(f"All participant/condition combinations have >= {min_trials} valid trials.")
        return True

    print(f"Below the {min_trials}-trial threshold (fit may come out noisy):")
    print(below_threshold.to_string())
    return False


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m driftlab_analysis.data_quality <path_to_csv>")
        sys.exit(1)

    df = load_csv(argv[0])
    ok = check_trial_counts(df)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
