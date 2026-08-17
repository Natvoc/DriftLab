# Stroop task

Classic color-word interference task: respond to the ink color a word is
printed in, ignoring what the word says.

## What it measures

Selective attention and inhibitory control. When the ink color and the word
meaning conflict (incongruent trials, e.g. the word "RED" printed in blue),
reading the word is automatic and interferes with naming the ink color,
producing slower and less accurate responses than when they match
(congruent trials).

## References

- Stroop, J. R. (1935). Studies of interference in serial verbal reactions.
  *Journal of Experimental Psychology*, 18(6), 643–662.
- MacLeod, C. M. (1991). Half a century of research on the Stroop effect:
  an integrative review. *Psychological Bulletin*, 109(2), 163–203.

## Parameters

- Practice trials: 8 (4 congruent / 4 incongruent, with feedback)
- Test trials: 48 (24 congruent / 24 incongruent, no feedback)
- Fixation duration: 500 ms
- Response timeout: 2000 ms
- Response key mapping (ink color → key, mnemonic by color initial):
  - red → `R`
  - green → `G`
  - blue → `B`
  - yellow → `Y`
- Expected effect size in the literature: ~50-150ms RT difference
  (incongruent slower than congruent)

## Data schema

Common columns (see `shared/js/data-export.js`): `participant_id`, `task`,
`block`, `trial_index`, `rt`, `correct`, `timestamp`.

Task-specific extra columns:
- `word`: the word shown (`"RED"`, `"GREEN"`, `"BLUE"`, `"YELLOW"`)
- `ink_color`: the actual ink color the word was rendered in
- `congruency`: `"congruent"` or `"incongruent"`
