#!/usr/bin/env bash

# Check database exists
sh /wait-for-databases.sh
sh /wait-for-kobo-cache-databases.sh

# Run collectstatic
python manage.py collectstatic --noinput
# Run migrate
python manage.py migrate

# Create uwsgi.ini

echo "Check uwsgi ini file"
if [ ! -f uwsgi.ini ]; then
	echo "Generate uwsgi.ini"
	envsubst < "uwsgi.ini.tpl" > "uwsgi.ini"
fi

echo "Executing command: $@"
exec "$@"
