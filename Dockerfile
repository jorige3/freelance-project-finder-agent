# Use a small Python base image
FROM python:3.12-slim AS builder

# Set environment variables for Python and uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency configuration files
COPY pyproject.toml uv.lock ./

# Build virtual environment with dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Build final production stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user first so we can use --chown
RUN useradd -u 10001 -m appuser

# Copy the virtual environment from the builder
COPY --chown=appuser:appuser --from=builder /app/.venv /app/.venv

# Copy source code
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser dashboard/ ./dashboard/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser pyproject.toml README.md ./

# Create data directory for database file persistence and set ownership
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Use non-root user
USER appuser

# Expose backend API and frontend dashboard ports
EXPOSE 8010
EXPOSE 8501

# Default health check for FastAPI
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8010/health || exit 1

# Default startup command (overridden in compose for the dashboard)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
