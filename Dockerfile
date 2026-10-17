# Multi-platform Python slim base image for Google Cloud Run / Container Hosting
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and governance assets
COPY src/ ./src/
COPY docs/ ./docs/
COPY domain-packs/ ./domain-packs/

# Expose default HTTP port
EXPOSE 8080

# Cloud Run dynamic PORT binding
CMD exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT}
