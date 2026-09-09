# Tasks

Last Updated: 2026-09-02

## Done

- [x] Ship fishing automation loop (`fishing.py`).
  - Delivered: Q1 2026
- [x] Ship thieving automation loop (`thieving.py`).
  - Delivered: Q1 2026
- [x] Fix Docker runtime entrypoint (`Dockerfile` CMD `python main.py` → `python -m bot.core`).
  - Delivered: 2026-04-03 (see `docs/HANDOFF-docker-entrypoint-20260403.md`)
- [x] Unify the Python version strategy across docs and Docker.
  - Delivered: 2026-09-02
  - Resolution: both Dockerfile stages, CI, and `pyproject.toml` now pin Python 3.10; README documents this as the single supported version with rationale.
- [x] Improve OCR correction and question-matching resilience.
  - Delivered: 2026-09-02
  - Resolution: `question_handler.py` now normalizes/lower-cases OCR text before matching and corrects the cleaned (not raw) text; `screen_processing.py` no longer raises on OCR/Tesseract failures. Covered by noisy-input fixtures in `tests/test_question_handler.py` and `tests/test_screen_processing.py`.
- [x] Add health and stuck-state recovery signals.
  - Delivered: 2026-09-02
  - Resolution: new `bot/health.py` `StuckStateMonitor` tracks stale OCR frames, repeated capture failures, and activity idle time for the fishing and thieving loops, and performs deterministic, logged recovery when thresholds are crossed. Covered by `tests/test_health.py`.

## Todo

- [ ] Add deterministic runtime checkpoint logging.
  - Priority: P2
  - Problem: long-session troubleshooting lacks enough timestamped checkpoints to explain failures.
  - Acceptance Criteria: key loop state (activity, location confidence, OCR confidence, last action) is logged periodically and summarized on failure.

- [ ] Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
