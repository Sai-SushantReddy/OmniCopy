#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

while ! python -c "
import psycopg2
from app.core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
conn.close()
" >/dev/null 2>&1
do
    sleep 2
done

echo "PostgreSQL is ready."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload