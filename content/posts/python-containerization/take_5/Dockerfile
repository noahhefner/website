# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY take_5/pyproject.toml take_5/uv.lock .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Run
# -----------------------
FROM python:3.14-alpine3.23 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/main.py main.py

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Run the program
CMD ["python", "main.py"]