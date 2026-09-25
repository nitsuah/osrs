# Tasks

> 🧭 [osrs](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

## Done

Condensed into `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated narrative here.

## Todo

- [ ] **[2027-Q1]** Give `StuckStateMonitor.recover()` a real skill-specific corrective action, and verify progress before resetting stale-frame state.
  - Priority: P2
  - Problem: two related gaps found in PR #37's review, both requiring live-game verification I can't do from this environment (no game client/display access), so deliberately not rushed:
    1. `recover()` only logs and resets counters; the calling loop's own fix (2026-09-09: a 1s backoff + `continue` before retrying) avoids immediately re-hitting the same failing capture path in the same iteration, but doesn't perform any actual corrective action (e.g. re-centering the camera, moving the character) the way the module's own docstring describes as the intent.
    2. `record_activity()` unconditionally resets `_stale_frame_count` whenever a loop takes an action (responds to a question, fishes, thieves), even if that action didn't verifiably change the game state. With `stale_frame_limit > 1`, a loop that keeps "acting" without real progress can therefore never trip stale-frame recovery.
  - Acceptance Criteria: a corrective action (e.g. `bot/camera.py`'s existing zoom/pan helpers) actually runs before `recover()` resets its counters, and `record_activity()` is only called after confirming the action produced a real state change — validated against the live game client, not just unit tests, since both changes affect real automation behavior.

- [ ] **[2027-Q1]** Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
