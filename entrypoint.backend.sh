#!/bin/sh

set -e

if [ -z "$ENVIRONMENT" ]; then
    echo "Error: ENVIRONMENT variable is not set. Exiting..."
    exit 1
fi

if [ -z "$DJANGO_PORT" ]; then
    echo "Error: DJANGO_PORT variable is not set. Exiting..."
    exit 1
fi

echo "Starting Django setup..."

python manage.py wait_for_db
python manage.py makemigrations --noinput
python manage.py migrate

if [ "$ENVIRONMENT" = "development" ]; then
    echo "Running Django development server on port $DJANGO_PORT..."
    python manage.py runserver 0.0.0.0:$DJANGO_PORT
elif [ "$ENVIRONMENT" = "production" ]; then
    echo "Running Django production server on port $DJANGO_PORT..."
    exec gunicorn --workers 9 --worker-class gthread --threads 2 core.wsgi:application --bind 0.0.0.0:$DJANGO_PORT
else
    echo "Error: Invalid ENVIRONMENT value. Must be 'development' or 'production'. Exiting..."
    exit 1
fi
