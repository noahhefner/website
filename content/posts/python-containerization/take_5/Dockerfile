# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Install dependencies
COPY take_5/pyproject.toml .
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Run
# -----------------------
FROM python:3.13-alpine3.22 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]