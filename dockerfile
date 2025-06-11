# Use a Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy pyproject.toml and uv.lock files
COPY pyproject.toml .
COPY uv.lock . 

# Install uv and git, and clean up apt lists
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && pip install uv \
    && rm -rf /var/lib/apt/lists/*

# Use uv to install dependencies based on pyproject.toml
RUN uv sync

COPY . . 

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the port your application will run on
EXPOSE 8080

# Command to run your Uvicorn application
# Use uv run directly to ensure uvicorn runs within the uv environment
CMD ["sh", "-c", "uv run uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"]