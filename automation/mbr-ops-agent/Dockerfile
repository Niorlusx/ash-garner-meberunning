FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
COPY apps ./apps

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "mistralai-workflows>=3.10" "pydantic>=2.0"

ENV PYTHONPATH=/app/apps/worker/src
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "worker.entrypoints.worker"]
