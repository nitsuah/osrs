# OSRS Bot Roadmap

> 🧭 [osrs](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2026 Q1 (fishing/thieving loops, OCR chat parsing, anti-bot responses, CI,
> Docker), 2026 Q2 (Python version reconciliation, OCR reliability, runtime health checks) and the 2026 Q3 P0 Docker
> fix (Python 3.12 everywhere, #44) are shipped — see [FEATURES](./FEATURES.md) / [CHANGELOG](../CHANGELOG.md). Every
> open 2026 Q3/Q4 item was carried into 2027 Q1 below.

## 2027 Q1 - Reliability & Skill Expansion (Planned)

### Committed *(carried from 2026 Q3)*

- [ ] Give stuck-state recovery a real skill-specific corrective action (basic monitoring/logging shipped in 2026 Q2; needs live-game validation — see `docs/TASKS.md`).
- [ ] Expand skill coverage to new modules such as woodcutting and mining.
- [ ] Add a deterministic simulation mode for behavior tests.

### Exploratory *(carried from 2026 Q4)*

- [ ] Evaluate multi-account orchestration safety boundaries.
- [ ] Evaluate operational controls for long-running autonomous sessions.
- [ ] **Session dashboard** — local-only web UI (served on `localhost`) that plots XP gained, actions per minute, and inventory events over a session timeline; a glance-view without tailing log files.
- [ ] **Behavioral profile system** — named automation profiles (`casual`, `focused`, `marathon`) that parametrize click variance, break frequency, and action cadence without editing source files.
