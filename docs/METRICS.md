# Metrics

## Core Metrics

| Metric              | Value | Notes                                      |
| ------------------- | ----- | ------------------------------------------ |
| Code Coverage | TBD | Could not re-measure on 2026-09-24: `docker build` fails on `main` (numpy 2.5.3 vs Python 3.10; see TASKS.md P0). The last measurement was 100% for `bot/camera.py`, `bot/compass.py` and `bot/utils.py` only (Docker run 2026-08-23, 25 tests). The test suite has grown since then. Command once fixed: `pytest tests/ --cov=bot --cov-report=term` |
| Lines of Code | 939 | Raw line count of all `.py` files under `bot/` (`wc -l`, 2026-09-24) |
| Python Files | 13 | `.py` files under `bot/` (2026-09-24) |
| Test Files | 8 | test_camera, test_checkpoint, test_compass, test_health, test_question_handler, test_screen_processing, test_smoke, test_utils (+ conftest.py) |
| Test Cases | 87 (static) | Static count of `def test_` in `tests/` (2026-09-24). Not executed because the Docker build is broken (see TASKS.md P0). |
| Config Files        | 1     | INI configuration file                     |
| Question Database   | 131   | Anti-bot question/answer pairs             |
| Skills Implemented  | 2     | Thieving and Fishing automation            |
| Dependencies | 9 | Pinned runtime packages in requirements.txt (2026-09-24) |

## Health

| Metric       | Value      | Notes                              |
| ------------ | ---------- | ---------------------------------- |
| Open Issues | 1 | `gh issue list` (2026-09-24) |
| Test Files | 8 | test_camera, test_checkpoint, test_compass, test_health, test_question_handler, test_screen_processing, test_smoke, test_utils (+ conftest.py) |
| Health Score | TBD | Docker build broken on `main` since #41 (2026-09-23); the old "A+ / 100" can't be backed until the P0 in TASKS.md is fixed |
| Last Updated | 2026-09-24 | PMO audit: static counts refreshed; Docker run blocked by build failure |
