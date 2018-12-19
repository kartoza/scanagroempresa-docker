#!/usr/bin/env bash

set -e

PGDATABASE=${DATA_PGDATABASE}
PGHOST=${DATA_PGHOST}
PGPORT=${DATA_PGPORT}
PGUSER=${DATA_PGUSER}
PGPASSWORD=${DATA_PGPASSWORD}

echo "Kobo cache database environment variables:"
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
	psql -d ${PGDATABASE} -c "create extension postgis;"
fi

>&2 echo "${PGDATABASE} are up - executing command"
