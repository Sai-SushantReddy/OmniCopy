#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

MAX_RETRIES=60
COUNT=0

until python -c "
import psycopg2
from app.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
conn.close()
" >/dev/null 2>&1
do
    COUNT=$((COUNT + 1))

    if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
        echo "ERROR: PostgreSQL connection failed after 120 seconds."
        exit 1
    fi

    echo "PostgreSQL not ready. Retrying... ($COUNT/$MAX_RETRIES)"
    sleep 2
done

echo "PostgreSQL is ready."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "${PORT:-8000}"
