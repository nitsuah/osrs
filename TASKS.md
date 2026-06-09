# Tasks

Last Updated: 2026-06-08

## In Progress

- [ ] Unify the Python version strategy across docs and Docker.
  - Priority: P1
  - Problem: README and Docker still disagree on the supported Python version.
  - Acceptance Criteria: the repo documents one supported version policy with rationale.

## Todo

- [ ] Improve OCR correction and question-matching resilience.
  - Priority: P1
  - Problem: OCR noise still hurts response quality in chat-triggered flows.
  - Acceptance Criteria: noisy OCR fixtures are covered and match precision improves.

- [ ] Add health and stuck-state recovery signals.
  - Priority: P1
  - Problem: long-running loops still lack strong runtime health checks.
  - Acceptance Criteria: low-health and stuck conditions trigger deterministic recovery actions.

- [ ] Add deterministic runtime checkpoint logging.
  - Priority: P2
  - Problem: long-session troubleshooting lacks enough timestamped checkpoints to explain failures.
  - Acceptance Criteria: key loop state (activity, location confidence, OCR confidence, last action) is logged periodically and summarized on failure.

- [ ] Expand skill modules behind stable automation primitives.
  - Priority: P2
  - Problem: new skill work depends on more reliable shared movement and interaction primitives.
  - Acceptance Criteria: new skills reuse common primitives and ship with module-level tests.
