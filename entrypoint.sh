#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the MySQL database to be ready
echo "Waiting for MySQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "MySQL started"

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Execute the container's main process (CMD)
exec "$@"
