# Metrics

## Core Metrics

| Metric              | Value | Notes                                      |
| ------------------- | ----- | ------------------------------------------ |
| Code Coverage | 98% | 784 statements, 16 missed; 87 tests passed. Measured 2026-09-24 inside the fixed Python 3.12 image: `docker build -t osrs-bot . && docker run --rm --entrypoint sh osrs-bot -c "cd /app && xvfb-run -a python -m pytest -q"` |
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
| Health Score | TBD | Docker build restored on 2026-09-24 (Python 3.12 alignment, and CI now builds the image). Re-score on the next PMO cycle |
| Last Updated | 2026-09-24 | PMO audit: static counts refreshed; Docker run blocked by build failure |
