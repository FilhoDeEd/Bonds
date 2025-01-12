#!/bin/sh

python manage.py wait_for_db
python manage.py makemigrations
python manage.py migrate

if [ "$ENVIRONMENT" = "development" ]; then
    echo 'Running Django development server...'
    python manage.py runserver 0.0.0.0:$DJANGO_PORT
else
    echo 'Running Django production server...'
    exec gunicorn --workers 9 --worker-class gthread --threads 2 base.wsgi:application --bind 0.0.0.0:$DJANGO_PORT
fi
