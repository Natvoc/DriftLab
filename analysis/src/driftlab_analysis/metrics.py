"""Trial-level metrics: RT, accuracy, and the classic Stroop effect.

All metrics here operate on "valid" trials only — see filter_valid_trials.
"""

# Trials outside this RT window are excluded before computing any metric:
# below MIN_VALID_RT_MS is an anticipatory response (too fast to reflect a
# real decision), above MAX_VALID_RT_MS is a likely lapse of attention.
# Trials with no response (rt is null/NaN, e.g. a timeout) are excluded by
# the same filter, since they aren't a valid decision either.
MIN_VALID_RT_MS = 200
MAX_VALID_RT_MS = 2000


def filter_valid_trials(df):
    return df[(df["rt"] >= MIN_VALID_RT_MS) & (df["rt"] <= MAX_VALID_RT_MS)]


def mean_rt(df, group_cols=None, correct_only=True):
    valid = filter_valid_trials(df)
    if correct_only:
        valid = valid[valid["correct"] == 1]
    if group_cols:
        return valid.groupby(group_cols)["rt"].mean()
    return valid["rt"].mean()


def accuracy(df, group_cols=None):
    valid = filter_valid_trials(df)
    if group_cols:
        return valid.groupby(group_cols)["correct"].mean()
    return valid["correct"].mean()


def stroop_effect(df):
    """Mean RT (incongruent) - mean RT (congruent), on correct, valid
    trials from the test block. Positive means the classic Stroop effect
    is present (incongruent trials slower than congruent)."""
    test = df[df["block"] == "test"]
    means = mean_rt(test, group_cols=["congruency"])
    return means["incongruent"] - means["congruent"]
