# Multi-stage Dockerfile for a Python application

# ================================
# Stage 1: Dependencies
# ================================
FROM python:3.11-slim-bookworm AS deps
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install dependencies, using a virtual environment
RUN apt-get update && apt-get install -y --no-install-recommends libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ================================
# Stage 2: Application
# ================================
FROM python:3.11-slim-bookworm AS app
WORKDIR /app

# Create non-root user for security
RUN groupadd --system appuser && useradd --system -g appuser appuser

# Copy application code
COPY . .

# Copy dependencies from the previous stage
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/app:/opt/venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose the application port - standardized to 5000
EXPOSE 5000

# Define entrypoint command
CMD ["python", "main.py"]