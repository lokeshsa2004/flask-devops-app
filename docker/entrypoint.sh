#!/bin/sh
set -e
cd /app
export FLASK_APP=app

if echo "${DATABASE_URL:-}" | grep -q "mysql"; then
  python docker/wait_for_mysql.py
fi

flask init-db

exec gunicorn -w 3 -b 0.0.0.0:8000 --access-logfile - --error-logfile - app:app
