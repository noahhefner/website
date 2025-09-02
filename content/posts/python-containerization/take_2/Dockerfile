# Start from Python Alpine image
FROM python:3.13-alpine3.22

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY take_2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]