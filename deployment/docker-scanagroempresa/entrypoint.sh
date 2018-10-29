#!/usr/bin/env bash

# Check database exists
sh /wait-for-databases.sh

# Run collectstatic
python manage.py collectstatic --noinput
# Run migrate
python manage.py migrate

echo "Executing command: $@"
exec "$@"
