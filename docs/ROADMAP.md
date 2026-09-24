# OSRS Bot Roadmap

Last Updated: 2026-09-24

## 2026 Q1 ✅

> Completed. Core fishing and thieving automation loops, OCR-driven chat parsing, anti-bot response support, core utility coverage, baseline CI, and Docker entrypoint fix all shipped.

## 2026 Q2 ✅

- [x] Reconcile the supported Python version across docs and Docker.
- [x] Improve OCR correction reliability and false-positive handling.
- [x] Add deterministic runtime health checks so long sessions can recover safely from stuck states.

## 2026 Q3 (Planned)

- [ ] **P0:** restore the Docker build: realign Python across Docker, CI and `pyproject.toml` after numpy 2.5.3 (#41) and the CI move to 3.12 (#42). See `docs/TASKS.md` (2026-09-24 PMO audit).
- [ ] Give stuck-state recovery a real skill-specific corrective action (basic monitoring/logging shipped in Q2; see `docs/TASKS.md`).
- [ ] Expand skill coverage to new modules such as woodcutting and mining.
- [ ] Add a deterministic simulation mode for behavior tests.

## 2026 Q4 (Exploratory)

- [ ] Evaluate multi-account orchestration safety boundaries.
- [ ] Evaluate operational controls for long-running autonomous sessions.
- [ ] **Session dashboard** — local-only web UI (served on `localhost`) that plots XP gained, actions per minute, and inventory events over a session timeline; gives the operator a glance-view without tailing log files.
- [ ] **Behavioral profile system** — named automation profiles (`casual`, `focused`, `marathon`) that parametrize click variance, break frequency, and action cadence; decouples behavior tuning from code changes and makes long-session patterns more varied without editing source files.
