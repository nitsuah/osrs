# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Fishing automation loop (`fishing.py`): F1 pause/resume, 60-second poll interval, inventory-full detection via OCR chat parsing.
- Thieving automation loop (`thieving.py`): F1 pause/resume, coin-pouch flush, Onyx rare-item halt, randomized action delay (0.5–0.8 s).
- `click_with_variance` in `actions.py`: ±5-pixel random offset on every click to mimic human interaction.
- `screen_processing.py`: full-screen PIL `ImageGrab` capture, NumPy conversion, Tesseract OCR chat-region extraction, timestamped screenshot save.
- `question_handler.py`: JSON knowledge base loader, `clean_question`, `correct_text` (TextBlob spell-check, in development), exact-match and keyword-match `lookup_response`.
- `compass.py` / `click_compass`: clicks the in-game compass to reset camera to North.
- `camera.py` / `check_and_zoom_in` + `hold_up_arrow`: scroll-based zoom and up-arrow camera tilt.
- `recorder.py`: pynput-based mouse-click recorder that saves coordinates to CSV for config setup.
- INI-based configuration (`bot/config.ini`) for coordinates, constants, Tesseract path, and logging.
- Docker-based test and coverage workflow; CI pipeline (lint → xvfb pytest → pyinstaller artifact).
- Anti-bot Q&A knowledge base (`questions.json`, 131 entries).
- 100% test coverage across `camera.py`, `compass.py`, `utils.py` (4 test files, 25 test cases).

### Fixed
- `Dockerfile` CMD changed from `python main.py` to `python -m bot.core` to match the actual entrypoint.

## [0.1.0] - 2026-01-01

### Added
- Project initialization with core bot structure.

[Unreleased]: https://github.com/nitsuah/osrs/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/osrs/releases/tag/v0.1.0