FROM python:3.13-slim

# Prevent Python from creating .pyc files
# and make logs appear immediately in Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory inside the container
WORKDIR /app

# Install Python dependencies first
# This improves Docker build caching.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY config.py .
COPY logger.py .
COPY main.py .
COPY etl ./etl

# Create runtime directories
RUN mkdir -p /app/data/raw /app/logs

# Run the ETL pipeline
CMD ["python", "main.py"]