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
nginx
gunicorn backend.wsgi -w 3 -b 127.0.0.1:8080
#uwsgi --ini /app/uwsgi.ini

sleep infinity

