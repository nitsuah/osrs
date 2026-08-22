# Metrics

## Core Metrics

| Metric              | Value | Notes                                      |
| ------------------- | ----- | ------------------------------------------ |
| Code Coverage       | 100%  | Comprehensive coverage. camera.py: 100%, compass.py: 100%, utils.py: 100%. All key bot functions tested. <br>**Docker-based test/coverage workflow enabled:**<br>Build: `docker build --no-cache -t osrs-test .`<br>Run: `docker run --rm -it osrs-test /opt/venv/bin/pytest --cov` |
| Lines of Code       | 396   | Python code in bot/ directory              |
| Python Files        | 11    | Core bot modules                           |
| Test Files          | 4     | test_smoke, test_utils, test_camera, test_compass |
| Test Cases          | 25    | All tests passing with comprehensive mocking |
| Config Files        | 1     | INI configuration file                     |
| Question Database   | 131   | Anti-bot question/answer pairs             |
| Skills Implemented  | 2     | Thieving and Fishing automation            |
| Dependencies        | 10    | Python packages (see requirements.txt)     |

## Health

| Metric       | Value      | Notes                              |
| ------------ | ---------- | ---------------------------------- |
| Open Issues  | 0          | GitHub issues                                   |
| Test Files   | 4          | test_smoke, test_utils, test_camera, test_compass |
| Health Score | A+ / 100   | 100% coverage; full CI pipeline                 |
| Last Updated | 2026-08-22 | Documentation audit                             |
