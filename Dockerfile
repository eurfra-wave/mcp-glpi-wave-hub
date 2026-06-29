# Multi-stage build for minimal image
FROM python:3.12-alpine AS builder

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy project files
WORKDIR /app
COPY pyproject.toml README.md ./

# Install dependencies
RUN uv sync --no-dev

# Runtime stage
FROM python:3.12-alpine

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY src/ /app/src/

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1

# Non-root user
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup
USER appuser

WORKDIR /app

# Expose SSE port
EXPOSE ${MCP_PORT:-8080}

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:${MCP_PORT:-8080}/health || exit 1

# Run with SSE transport
CMD ["python", "-m", "src.main", "--sse"]