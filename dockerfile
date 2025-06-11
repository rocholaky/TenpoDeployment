FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates

RUN python -m pip install --upgrade pip

RUN pip install .

COPY api/ api/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8080}"]
