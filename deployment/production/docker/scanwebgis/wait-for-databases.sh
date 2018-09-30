#!/usr/bin/env bash

set -e

echo "Database environment variables:"
echo "PGDATABASE=$PGDATABASE"
echo "PGHOST=$PGHOST"
echo "PGPORT=$PGPORT"
echo "PGUSER=$PGUSER"
echo "PGPASSWORD=$PGPASSWORD"

until psql -l; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

if psql -d ${PGDATABASE} -c '\l'; then
	>&2 echo "${PGDATABASE} is available"
else
	>&2 echo "${PGDATABASE} is unavailable. Creating a new one."
	createdb ${PGDATABASE}
fi

>&2 echo "${PGDATABASE} are up - executing command"
