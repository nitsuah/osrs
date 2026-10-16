# Tasks

> 🧭 [osrs](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-10-01

## Done

Condensed into `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history) — see those
files rather than a duplicated narrative here.

## In Progress

## Todo

- [ ] **[2027-Q1]** Validate stuck-state recovery in a live game session.
  - Priority: P2
  - Context: the code shipped in #47 (skill-specific `corrective_action` for fishing and thieving, verified-only stale-frame resets), but it has only been unit-tested. Nobody has watched a stuck loop recover against a real client.
  - Acceptance Criteria: a fishing and a thieving loop are forced into a stuck state with a real client running; each recovers via its corrective action without a manual restart; the result is recorded here.

- [ ] Bump the `nltk` pin once a patched release ships (#39, GHSA-8mgp-746c-j5xp).
  - Priority: P3
  - Type: Security · Confidence: High
  - Problem: `nltk==3.10.3` in `requirements.txt` is flagged High (CVSS 7.0) by Dependabot alerts #6/#7, and the pip-audit CI step runs with `continue-on-error: true` (PR #38) to work around it. On 2026-10-01 PyPI still listed 3.10.3 as the newest release, so it remains blocked upstream.
  - Acceptance Criteria: `nltk` is bumped to a patched version, the `continue-on-error` on pip-audit is removed, and #39 is closed.

- [ ] **[2027-Q1]** Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
