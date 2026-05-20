# Start from uv image
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY take_3/pyproject.toml take_3/uv.lock .

# Install Python modules
RUN uv sync --no-cache

# Copy application code
COPY src/main.py main.py

# Ensure venv is used for all Python calls
ENV PATH="/app/.venv/bin:$PATH"

# Run the program
CMD ["python", "main.py"]