# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `bot/health.py` `StuckStateMonitor`: tracks stale OCR chat frames, consecutive screen-capture failures, and loop idle time for `fishing.py`/`thieving.py`, and performs deterministic, logged recovery when a loop looks stuck.
- Tests for the above: `tests/test_health.py`, `tests/test_question_handler.py`, `tests/test_screen_processing.py` (including noisy-OCR-input fixtures).
- `bot/checkpoint.py` `CheckpointLogger`: periodic (default 60s) structured checkpoint log line for `fishing.py`/`thieving.py` (elapsed runtime, last action, idle time, `StuckStateMonitor` counters), plus a capped recent-action ring buffer that `summarize_failure()` dumps to an error-level log when an unhandled exception ends the loop. Covered by `tests/test_checkpoint.py`.

### Changed

- `Dockerfile` app stage pinned to `python:3.10-slim-bookworm` (was `3.11`), matching the deps stage, CI, and `pyproject.toml`; README now documents one supported Python version instead of two.
- `question_handler.py`: `lookup_response` now normalizes (lower-case, whitespace-collapsed) OCR text before comparing, and corrects the *cleaned* question instead of the raw OCR string, fixing a case-sensitivity bug that silently defeated exact-match lookups. `clean_question` now strips the "click here to continue" prompt boilerplate case- and whitespace-insensitively (was an exact string match) and `lookup_response` no longer raises if `questions.json` has a malformed `questions` value or entry.
- `screen_processing.py`: `capture_and_process_chat` no longer raises on Tesseract/OCR failures; it logs and returns an empty chat string so a transient OCR error can't crash a long-running loop. It now also returns an explicit `ocr_ok` flag (2026-09-09) so callers can distinguish an actual OCR failure from a legitimately empty chat region — both previously collapsed into `record_frame("")`, which reset the stuck-state monitor's capture-failure counter on every call and meant a persistent Tesseract failure could never trip `capture_failure_limit`.
- `fishing.py` / `thieving.py`: route an OCR failure to `health_monitor.record_capture_failure()` instead of `record_frame("")`; back off 1s and skip the rest of the loop iteration after `health_monitor.recover()` instead of immediately retrying the same capture path that was just declared stuck.

### Added (from initial release)

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