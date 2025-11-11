#!/bin/bash
# Heroku startup script

# Run database migrations if needed
# python manage.py migrate

# Start the web server
uvicorn web_api:app --host 0.0.0.0 --port ${PORT:-8000}
