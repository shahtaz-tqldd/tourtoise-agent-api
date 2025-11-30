#!/bin/sh
set -e

APP_ENV=${APP_ENV:-dev}
PORT=${PORT:-5000}

echo "App Environment: $APP_ENV"

if [ "$APP_ENV" = "prod" ]; then
  echo "Running database migrations..."
  alembic upgrade head

  echo "Starting server with Uvicorn on port 8080"
  exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    --workers 4 \
    --log-level info \
    --access-log \
    --no-use-colors \
    --proxy-headers
else
  echo "Running database migrations (dev mode)..."
  alembic upgrade head || echo "Skipping migrations (maybe DB not ready?)"

  echo "Starting server with Uvicorn on port $PORT (reload enabled)"
  exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --reload \
    --log-level debug \
    --no-use-colors \
    --proxy-headers
fi
