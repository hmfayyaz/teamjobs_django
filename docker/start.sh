#!/bin/bash

cd /app || exit

lookup_ips() {
  python <<EOF
import sys

from dns import resolver

ip_addresses = []
for name in "${@}".split():
  try:
    ip_addresses.extend(a.address for a in resolver.resolve(name, 'A'))
  except (resolver.NXDOMAIN, resolver.NoNameservers):
    print("*")
    sys.exit(0)

if ip_addresses:
  print(",".join(ip_addresses))
else:
  print("*")

sys.exit(0)
EOF
}

if [[ "$DJANGO_ENV" == "development" ]]; then
    echo "Running development server"
    python manage.py runserver 0.0.0.0:8000
    exit 0
fi

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server)" # /beat/worker/flower)"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "server" ]; then
    PROXY_IP=$(lookup_ips ${PROXY_HOST})
    if [ "$DJANGO_DEBUG" = "true" ]; then
        gunicorn \
            --bind 0.0.0.0:8000 \
            --workers 2 \
            --worker-class gevent \
            --log-level DEBUG \
            --access-logfile "-" \
            --error-logfile "-" \
            teamjobsbackend.wsgi
    else
        gunicorn \
            --forwarded-allow-ips=${PROXY_IP} \
            --bind 0.0.0.0:8000 \
            --workers 2 \
            --worker-class gevent \
            --log-level INFO \
            --access-logfile "-" \
            --error-logfile "-" \
            teamjobsbackend.wsgi
    fi
#elif [ "$PROCESS_TYPE" = "beat" ]; then
#    celery \
#        --app teamjobsbackend.celery_app \
#        beat \
#        --loglevel INFO \
#        --scheduler django_celery_beat.schedulers:DatabaseScheduler
#elif [ "$PROCESS_TYPE" = "flower" ]; then
#    celery \
#        --app teamjobsbackend.celery_app \
#        flower \
#        --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
#        --loglevel INFO
#elif [ "$PROCESS_TYPE" = "worker" ]; then
#    celery \
#        --app teamjobsbackend.celery_app \
#        worker \
#        --loglevel INFO
fi
