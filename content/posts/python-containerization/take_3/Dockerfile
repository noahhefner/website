# Start from uv image
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements and install
COPY take_3/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]