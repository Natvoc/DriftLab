# DriftLab

A browser-based battery of cognitive psychophysics tasks (Stroop, Flanker, N-back, and more) paired with a Python analysis pipeline that uses drift-diffusion modeling (DDM) to separate processing speed from decision threshold.

🚧 **Work in progress — Fase 1 (MVP).** Stroop and a simple RT task are playable; DDM fitting comes in a later phase.

## What is this, and why?

Tasks like the ones below ask you to respond as fast and accurately as
possible to a simple stimulus — a color word, a row of arrows, a sequence
of letters to remember. Cognitive science has used tasks like these for
decades because they're cheap to run and surprisingly revealing about how
the mind processes information.

Most analyses stop at averages: mean reaction time and percent correct per
condition. But an average hides the thing that's actually interesting. Two
people — or the same person on two different days — can post the same
average reaction time for opposite reasons: one is fast because they're
genuinely quick at gathering evidence for a decision, the other is fast
because they're willing to commit to a shakier answer. A plain average
can't tell those apart; it only sees the outcome, not the process behind
it.

That's what a drift-diffusion model (DDM) is for. Instead of treating each
trial as a single RT number, it models a decision as noisy evidence
building up over time toward one of two thresholds, and fits two separate
quantities from the full shape of your reaction times and errors: how fast
evidence accumulates (**drift rate**, roughly "processing speed") and how
much evidence you require before committing to an answer (**decision
threshold**, roughly "caution"). Two conditions that look identical on RT
alone can turn out to differ cleanly on one of these and not the other.

DriftLab exists to run that idea end to end, in the open: play a battery
of classic cognitive tasks in the browser (no install, no lab equipment,
no EEG), export your own data, and feed it into a reproducible Python
pipeline that fits a DDM to it — checking whether well-known effects,
starting with the classic Stroop interference effect, show up as a
difference in drift rate, threshold, both, or neither, and whether that
matches what's been published.

You don't need to run any code to get the idea — the rest of this README
is for anyone who wants to try the tasks or run the analysis themselves.

## Play the demo

Browsers block `fetch()` on `file://` for CORS reasons, so serve the repo over a local static server instead of opening `index.html` directly:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/` and pick a task.

## Run the analysis pipeline

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r analysis/requirements.txt
pip install -e analysis        # installs driftlab_analysis in editable mode
```

Run the tests:

```bash
pytest analysis/tests/
```

Run the notebook:

```bash
jupyter notebook analysis/notebooks/01_stroop_basic_analysis.ipynb
```

It uses real data from `analysis/data/raw/` if any is present (exported from the browser tasks), and falls back to a versioned synthetic sample otherwise — so it runs out of the box without playing the task first.

## Architecture

Each task lives in its own self-contained folder under `experiments/`, using a shared data export module (`shared/js/data-export.js`) so any task's CSV export can be loaded by the analysis pipeline without task-specific code. See each task's own `README.md` for what it measures and its parameters.

## License

MIT — see `LICENSE`.
