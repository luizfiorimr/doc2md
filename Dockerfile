FROM python:3.13-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  FLASK_APP=main.py \
  FLASK_ENV=production \
  WORKERS=4 \
  TIMEOUT=120

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  curl \
  graphicsmagick \
  ghostscript \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies and gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 777 uploads

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Run gunicorn with environment variables
CMD gunicorn --bind 0.0.0.0:5000 --workers ${WORKERS} --timeout ${TIMEOUT} main:app

