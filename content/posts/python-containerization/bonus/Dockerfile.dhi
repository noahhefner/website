# -----------------------
# Stage 1: Build
# -----------------------
FROM dhi.io/uv:0-debian13-dev AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY bonus/pyproject.toml bonus/uv.lock .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM dhi.io/python:3 AS runner

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