FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for web API
RUN pip install --no-cache-dir fastapi uvicorn[standard]

# Copy source code
COPY src/ ./src/
COPY web_api.py .
COPY .env .

# Expose port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "8000"]
