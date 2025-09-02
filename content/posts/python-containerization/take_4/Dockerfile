# Start from Python Alpine image
FROM python:3.13-alpine3.22

# Copy the uv binary from the distroless uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements and install
COPY take_4/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]