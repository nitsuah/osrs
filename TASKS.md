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
  - Delivered: 2026-09-02, hardened 2026-09-09
  - Resolution: new `bot/health.py` `StuckStateMonitor` tracks stale OCR frames, repeated capture failures, and activity idle time for the fishing and thieving loops, and performs deterministic, logged recovery when thresholds are crossed. Covered by `tests/test_health.py`. 2026-09-09: fixed a gap found in review — `capture_and_process_chat` collapsed "OCR raised an exception" and "chat region is legitimately empty" into the same `""` return, so a persistent Tesseract failure reset `record_capture_failure`'s counter on every call and could never reach `capture_failure_limit`. Now returns an explicit `ocr_ok` flag; both loops route an OCR failure to `record_capture_failure()` instead of `record_frame("")`.

## Todo

- [ ] Give `StuckStateMonitor.recover()` a real skill-specific corrective action, and verify progress before resetting stale-frame state.
  - Priority: P2
  - Problem: two related gaps found in PR #37's review, both requiring live-game verification I can't do from this environment (no game client/display access), so deliberately not rushed:
    1. `recover()` only logs and resets counters; the calling loop's own fix (2026-09-09: a 1s backoff + `continue` before retrying) avoids immediately re-hitting the same failing capture path in the same iteration, but doesn't perform any actual corrective action (e.g. re-centering the camera, moving the character) the way the module's own docstring describes as the intent.
    2. `record_activity()` unconditionally resets `_stale_frame_count` whenever a loop takes an action (responds to a question, fishes, thieves), even if that action didn't verifiably change the game state. With `stale_frame_limit > 1`, a loop that keeps "acting" without real progress can therefore never trip stale-frame recovery.
  - Acceptance Criteria: a corrective action (e.g. `bot/camera.py`'s existing zoom/pan helpers) actually runs before `recover()` resets its counters, and `record_activity()` is only called after confirming the action produced a real state change — validated against the live game client, not just unit tests, since both changes affect real automation behavior.

- [ ] Add deterministic runtime checkpoint logging.
  - Priority: P2
  - Problem: long-session troubleshooting lacks enough timestamped checkpoints to explain failures.
  - Acceptance Criteria: key loop state (activity, location confidence, OCR confidence, last action) is logged periodically and summarized on failure.

- [ ] Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
