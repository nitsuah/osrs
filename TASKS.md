# Tasks

## Done

- [x] Implemented fishing and thieving automation modules.
- [x] Added OCR/chat parsing and question-response utilities.
- [x] Added automated tests for `camera.py`, `compass.py`, `utils.py`, and smoke coverage.
- [x] Added CI workflow for baseline quality checks.

## In Progress

- [ ] P0 | Bug | Confidence: High | Fix Docker runtime entrypoint.
  - Problem: Container starts with `python main.py`, but no `main.py` exists in repo root.
  - Impact: Docker deployment path is broken despite successful image build.
  - Acceptance Criteria: Container starts successfully and executes the documented bot entrypoint.
  - Dependencies: None.

- [ ] P1 | Tech Debt | Confidence: High | Unify Python version strategy across docs and Docker.
  - Problem: README states Python 3.13 while Docker stages use Python 3.10 and 3.11.
  - Impact: Inconsistent runtime behavior and avoidable troubleshooting.
  - Acceptance Criteria: README and Docker specify one supported version policy with explicit rationale.
  - Dependencies: Docker entrypoint fix.

## Todo

- [ ] P1 | Feature | Confidence: Medium | Improve OCR correction and question matching resilience.
  - Problem: OCR noise still affects response quality in chat-triggered flows.
  - Impact: Increases missed or incorrect anti-bot responses.
  - Acceptance Criteria: Add test fixtures for noisy OCR text and improve match precision against known prompts.
  - Dependencies: None.

- [ ] P1 | Reliability | Confidence: Medium | Add health and stuck-state recovery signals.
  - Problem: Bot can continue loops without robust runtime health checks.
  - Impact: Higher failure risk during extended sessions.
  - Acceptance Criteria: Detect low-health/stuck conditions and trigger deterministic recovery actions.
  - Dependencies: OCR reliability improvements.

- [ ] P2 | Feature | Confidence: Low | Expand skill modules (woodcutting, mining) behind stable automation primitives.
  - Problem: Planned skill expansion depends on robust shared movement and interaction primitives.
  - Impact: Premature expansion may amplify maintenance overhead.
  - Acceptance Criteria: New skills reuse common primitives and include module-level tests.
  - Dependencies: Health recovery and OCR reliability tasks.

