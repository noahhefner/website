# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml
COPY take_3/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Run
# -----------------------
FROM python:3.13-alpine3.22 AS runner

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