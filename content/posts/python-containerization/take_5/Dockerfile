# -----------------------
# Stage 1: Build
# -----------------------
FROM python:3.13-alpine3.22 AS builder

# Copy the uv binary from the distroless uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements and install dependencies
COPY take_5/pyproject.toml .
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
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
