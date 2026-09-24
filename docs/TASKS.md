# Tasks

Last Updated: 2026-09-24

## Done

Condensed into `docs/ROADMAP.md` (milestones), `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated narrative here.

## Todo

- [ ] **P0: Docker build on `main` is broken. `numpy==2.5.3` requires Python >=3.12, but the Dockerfile uses 3.10.**
  - Priority: P0 · Type: Bug · Confidence: High
  - Problem: found in the 2026-09-24 PMO audit. `docker build -t osrs-test .` (the README/METRICS test path) fails at `pip install -r requirements-dev.txt` with `No matching distribution found for numpy==2.5.3`. pip reports that numpy 2.3.x/2.4.x require Python >=3.11 and 2.5.x require >=3.12. Dependabot #41 bumped numpy from 2.2.6 to 2.5.3 on 2026-09-23. #42, the same day, moved CI's `setup-python` to 3.12, so #41's checks passed. Neither PR touched the Dockerfile (`python:3.10-slim-bookworm` in both stages), `pyproject.toml` (`target-version = "py310"`), or README, which still says "Python 3.10 is the single supported version, used consistently in CI, Docker … and local tooling".
  - Why it matters: the only documented way to run tests and the bot in a container is broken on `main`. The single-version policy in README is now false, because CI uses 3.12 while Docker and tooling use 3.10.
  - Acceptance Criteria: choose one Python version and apply it everywhere. Either (a) move both Dockerfile stages and `pyproject.toml` to 3.12, keeping numpy 2.5.3, or (b) revert CI to 3.10 and pin `numpy<2.3`, with a Dependabot `ignore` rule so it doesn't re-bump. Then `docker build -t osrs-test . && docker run --rm osrs-test xvfb-run -a /opt/venv/bin/python -m pytest --cov` passes, the README Dependencies bullet matches, and a Docker build check runs in CI so Dependabot bumps can't break the image silently again.

- [ ] Give `StuckStateMonitor.recover()` a real skill-specific corrective action, and verify progress before resetting stale-frame state.
  - Priority: P2
  - Problem: two related gaps found in PR #37's review, both requiring live-game verification I can't do from this environment (no game client/display access), so deliberately not rushed:
    1. `recover()` only logs and resets counters; the calling loop's own fix (2026-09-09: a 1s backoff + `continue` before retrying) avoids immediately re-hitting the same failing capture path in the same iteration, but doesn't perform any actual corrective action (e.g. re-centering the camera, moving the character) the way the module's own docstring describes as the intent.
    2. `record_activity()` unconditionally resets `_stale_frame_count` whenever a loop takes an action (responds to a question, fishes, thieves), even if that action didn't verifiably change the game state. With `stale_frame_limit > 1`, a loop that keeps "acting" without real progress can therefore never trip stale-frame recovery.
  - Acceptance Criteria: a corrective action (e.g. `bot/camera.py`'s existing zoom/pan helpers) actually runs before `recover()` resets its counters, and `record_activity()` is only called after confirming the action produced a real state change — validated against the live game client, not just unit tests, since both changes affect real automation behavior.

- [ ] Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
