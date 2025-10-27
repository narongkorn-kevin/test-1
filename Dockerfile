# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Environment for reliable, quiet, non-interactive builds and headless matplotlib
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg

WORKDIR /app

# System packages needed by some Python wheels at runtime (matplotlib fonts/png/jpeg)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libfreetype6 libpng16-16 libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 8080

# Default command: production WSGI server
CMD ["gunicorn", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:8080", "app:app"]


