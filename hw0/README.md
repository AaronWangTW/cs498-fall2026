# HW0 — Perspective, Homography, Stereo

Initial Fall 2026 development package. It refactors the reusable ideas from CS498 MP1 and the stereo-matching portion of CS498 MP2 into independent, testable modules.

The old basketball-court assets are intentionally not copied. The final assignment will use a tennis-court scene; image correspondences, court dimensions, camera calibration, and the insertable object will be included before release.

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cs498-hw0 check
pytest
```

The environment check and public tests do not require the final tennis dataset.

## Package boundaries

- `src/cs498_hw0/`: student-facing starter API. Required functions deliberately raise `NotImplementedError` until implemented.
- `tests/`: public interface and starter-contract checks.
- `latex/main.tex`: initial handout draft.
- `data/`: acquisition and provenance notes; large datasets are not committed.
- `outputs/`: generated results; only `.gitkeep` is tracked.

Keep all required public function signatures unchanged so the released tests and grading tools can import your work.
