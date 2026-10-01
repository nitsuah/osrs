# Tasks

> 🧭 [osrs](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-10-01

## Done

Condensed into `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated narrative here.

## In Progress

- [ ] **[2027-Q1]** Give `StuckStateMonitor.recover()` a real skill-specific corrective action, and verify progress before resetting stale-frame state.
  - Priority: P2
  - Problem: two related gaps found in PR #37's review, both requiring live-game verification I can't do from this environment (no game client/display access), so deliberately not rushed:
    1. `recover()` only logs and resets counters; the calling loop's own fix (2026-09-09: a 1s backoff + `continue` before retrying) avoids immediately re-hitting the same failing capture path in the same iteration, but doesn't perform any actual corrective action (e.g. re-centering the camera, moving the character) the way the module's own docstring describes as the intent.
    2. `record_activity()` unconditionally resets `_stale_frame_count` whenever a loop takes an action (responds to a question, fishes, thieves), even if that action didn't verifiably change the game state. With `stale_frame_limit > 1`, a loop that keeps "acting" without real progress can therefore never trip stale-frame recovery.
  - Acceptance Criteria: a corrective action (e.g. `bot/camera.py`'s existing zoom/pan helpers) actually runs before `recover()` resets its counters, and `record_activity()` is only called after confirming the action produced a real state change — validated against the live game client, not just unit tests, since both changes affect real automation behavior.
  - Done in PR #47: added `corrective_action` callback to `recover()` and `verified` param to `record_activity()`. Both fishing/thieving skills now pass camera re-centering as corrective action. Question responses use `verified=True`, skill actions use `verified=False`. Tests cover new behavior.
  - Remaining: the live-game validation in the Acceptance Criteria has not run yet (no game client in the automation environment). Check this off once a live session confirms the corrective action fires and stale frames stop resetting on unverified actions.

## Todo

- [ ] Bump the `nltk` pin once a patched release ships (#39, GHSA-8mgp-746c-j5xp).
  - Priority: P3
  - Type: Security · Confidence: High
  - Problem: `nltk==3.10.3` in `requirements.txt` is flagged High (CVSS 7.0) by Dependabot alerts #6/#7, and the pip-audit CI step runs with `continue-on-error: true` (PR #38) to work around it. On 2026-10-01 PyPI still listed 3.10.3 as the newest release, so it remains blocked upstream.
  - Acceptance Criteria: `nltk` is bumped to a patched version, the `continue-on-error` on pip-audit is removed, and #39 is closed.

- [ ] **[2027-Q1]** Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
