#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL started"

# Apply migrations and start the app
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
