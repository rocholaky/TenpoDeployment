FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency files early to leverage Docker cache
COPY pyproject.toml .
COPY uv.lock .

# 1. Update APT and install system tools (curl, certs only)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates

RUN python -m pip install --upgrade pip

# 2. Install uv
RUN pip install uv

# 5. Install Python dependencies with uv
RUN uv sync

# 6. Copy application code
COPY api/ api/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8080

# Run the app
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
