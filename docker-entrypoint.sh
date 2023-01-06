#!/bin/sh

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate

# Start Celery
echo "Starting Celery"
celery -A api multi start worker

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000