# OSRS Bot Roadmap

## 2026 Q1 (Completed)

- [x] Implemented core automation loops for thieving and fishing
- [x] Added OCR-driven chat parsing and anti-bot response pipeline
- [x] Added core utility test coverage for camera, compass, and utility modules
- [x] Added baseline CI workflow

## 2026 Q2 (In Progress)

- [ ] Stabilize container runtime (current image entrypoint references missing `main.py`)
- [ ] Reconcile runtime version strategy (README Python 3.13 vs Docker 3.10/3.11)
- [ ] Improve OCR correction reliability and false-positive handling

## 2026 Q3 (Planned)

- [ ] Implement health monitoring and recovery actions (HP checks, stuck detection, safe reset)
- [ ] Expand skill coverage (woodcutting, mining)
- [ ] Add deterministic simulation mode for behavior tests without live client dependency

## 2026 Q4 (Exploratory)

- [ ] Evaluate multi-account orchestration safety boundaries
- [ ] Evaluate operational controls for long-running autonomous sessions

