# Multi-stage Dockerfile for a Python application

# ================================
# Stage 1: Dependencies
# ================================
FROM python:3.10-slim-bookworm AS deps
WORKDIR /app

# Copy dependency definitions
COPY requirements.txt .
COPY requirements-dev.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
	libgl1-mesa-glx tesseract-ocr python3-venv python3-pip && \
	rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements-dev.txt

# ================================
# Stage 2: Application
# ================================
# Pinned to the same minor version as the deps stage and CI (3.10) so the
# interpreter that builds/tests wheels is the one that runs them. See
# README.md "Dependencies" for the version policy rationale.
FROM python:3.10-slim-bookworm AS app
WORKDIR /app

# tesseract-ocr: required at runtime by pytesseract (bot/skills/screen_processing.py).
# xvfb: provides a virtual DISPLAY so pyautogui/mouseinfo can be imported/tested
# headlessly, matching the CI job's `xvfb-run -a pytest` step.
RUN apt-get update && apt-get install -y --no-install-recommends \
	tesseract-ocr xvfb xauth python3-tk && \
	rm -rf /var/lib/apt/lists/*

# Xvfb (run as the non-root appuser below) refuses to create its own socket
# directory under /tmp, so it must already exist with the standard X11 mode.
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Create non-root user for security. --create-home is needed so python-xlib
# (a pyautogui dependency, imported for its DISPLAY/mouseinfo check) has a
# home directory to look for ~/.Xauthority in -- see the empty Xauthority
# file created below.
RUN groupadd --system appuser && useradd --system --create-home -g appuser appuser

# python-xlib raises immediately if ~/.Xauthority doesn't exist at all, even
# though Xvfb here runs without cookie-based auth -- an empty file satisfies
# the "does it exist" check.
RUN touch /home/appuser/.Xauthority && chown appuser:appuser /home/appuser/.Xauthority

# Copy application code
COPY . .

# Copy dependencies from the previous stage
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/app:/opt/venv/bin:$PATH"

# appuser needs write access to run/read the app directory (pytest cache,
# debug screenshots under bot/questions, etc.) when this image is used for
# `docker run ... pytest` as documented in README.md.
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port - standardized to 5000
EXPOSE 5000

# Define entrypoint command
CMD ["python", "-m", "bot.core"]