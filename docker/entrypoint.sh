#!/bin/bash

# entrypoint.sh file of Dockerfile

# Section 1- Bash options
set -o errexit
set -o pipefail
set -o nounset

# Section 2: Health of dependent services
postgres_ready() {
  python <<END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${DJANGO_POSTGRES_DB}",
        user="${DJANGO_POSTGRES_USER}",
        password="${DJANGO_POSTGRES_PASSWORD}",
        host="${DJANGO_DATABASE_HOST}",
        port="${DJANGO_DATABASE_PORT}",
    )
except OperationalError:
    sys.exit(-1)
END
}

if [[ "${DJANGO_ENV}" = "production" ]]; then
  until postgres_ready; do
    echo >&2 "Waiting for PostgreSQL to become available..."
    sleep 5
  done
  echo >&2 "PostgreSQL is available"
fi

# Section 3- Idempotent Django commands
cd /app
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

exec "$@"
