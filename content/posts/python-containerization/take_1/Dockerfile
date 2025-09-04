# Start from Ubuntu
FROM ubuntu:24.04

# Install Python, pip, and venv
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python3 -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt
COPY take_1/requirements.txt .

# Install Python modules
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]