# Simple RT task

Press a key as fast as possible when a stimulus appears.

## What it measures

Baseline simple reaction time — the floor for how fast someone can detect a
stimulus and initiate a motor response, with no decision or discrimination
involved. Useful as a reference point against choice-RT tasks (Stroop,
Flanker) and as a first candidate for a 2-boundary drift-diffusion fit in
Fase 2, since it's the simplest possible decision (respond vs. not yet).

## References

- Luce, R. D. (1986). *Response Times: Their Role in Inferring Elementary
  Mental Organization*. Oxford University Press — classic reference on
  simple vs. choice RT.

## Parameters

- Practice trials: 5
- Test trials: 30
- Fixation duration: 500 ms
- Foreperiod (blank screen before stimulus onset): random, 1000-3000 ms
  (discourages anticipatory responses)
- Response timeout: 2000 ms
- Response key: `Space`
- Expected RT range: ~150-300ms for genuine simple RT (much faster than
  choice-RT tasks like Stroop)

## Data schema

Common columns (see `shared/js/data-export.js`): `participant_id`, `task`,
`block`, `trial_index`, `rt`, `correct`, `timestamp`.

No task-specific extra columns — intentionally the simplest possible task,
used as a smoke test for the plugin architecture.
