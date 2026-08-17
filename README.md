# DriftLab

A browser-based battery of cognitive psychophysics tasks (Stroop, Flanker, N-back, and more) paired with a Python analysis pipeline that uses drift-diffusion modeling (DDM) to separate processing speed from decision threshold.

🚧 **Work in progress — Fase 1 (MVP).** Stroop and a simple RT task are playable; DDM fitting comes in a later phase.

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
