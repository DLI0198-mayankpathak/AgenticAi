FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for web API
RUN pip install --no-cache-dir fastapi uvicorn[standard] gunicorn

# Copy source code
COPY src/ ./src/
COPY web_api.py .

# Optional: Copy .env if exists (for local testing)
# In production, use environment variables from the platform
COPY .env* ./

# Expose port (configurable via PORT env var)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the API
# Use PORT environment variable if available (for platforms like Heroku, Railway)
CMD uvicorn web_api:app --host 0.0.0.0 --port ${PORT:-8000}
