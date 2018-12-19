#!/usr/bin/env bash

# Check database exists
sh /wait-for-databases.sh
sh /wait-for-kobo-cache-databases.sh

# Run collectstatic
python manage.py collectstatic --noinput
# Run migrate
python manage.py migrate

echo "Executing command: $@"
exec "$@"
