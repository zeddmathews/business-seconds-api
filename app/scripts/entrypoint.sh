#!/bin/bash
set -e

echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

echo "✅ PostgreSQL is ready. Running holiday seed script..."
python app/scripts/seed_holidays.py

echo "🚀 Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 app.main:app --reload