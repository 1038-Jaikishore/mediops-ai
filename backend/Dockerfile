# --- Stage 1: Build virtual environment ---
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Clean runtime image ---
FROM python:3.12-slim AS runner

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy source code and migrations
COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini .
COPY start.sh .

# Ensure start script is executable
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]
