# =========================================================
# Kuhi Anime API — Dockerfile for Railway
# =========================================================
FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Layer caching — install deps first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Railway injects $PORT at runtime; fall back to 8000 locally
ENV PORT=8000
EXPOSE 8000

# Healthcheck — Kuhi exposes a root route
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://127.0.0.1:${PORT}/ || exit 1

# Bind to Railway's dynamic port
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT}"]
