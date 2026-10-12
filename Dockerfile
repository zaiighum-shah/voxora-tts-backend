FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && pip install --no-cache-dir --force-reinstall -r requirements.txt \
    && apt-get purge -y git \
    && rm -rf /var/lib/apt/lists/*

COPY main.py .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
