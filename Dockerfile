FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install uv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# Create non-root user for security
RUN groupadd -r paywallbot && useradd -r -g paywallbot paywallbot

WORKDIR /app

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies and sync environment as root
RUN uv sync --frozen || uv sync

# Copy project files (exclude unnecessary files like .env, .git, etc.)
COPY bot.py config.py domains.txt ./
COPY cogs ./cogs

# Create uv cache directory and set permissions
RUN mkdir -p /home/paywallbot/.cache/uv && \
    chown -R paywallbot:paywallbot /app /home/paywallbot/.cache

# Switch to non-root user
USER paywallbot

# Entrypoint: run bot using uv's environment
CMD ["uv", "run", "python", "bot.py"]

