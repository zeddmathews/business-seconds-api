#!/bin/bash
set -e

if lsof -i :5432 >/dev/null 2>&1; then
    echo "Port 5432 is already in use. Likely due to a local PostgreSQL instance."
    echo "Please stop the local service or change the port in docker-compose.yml in service:db:ports"
    exit 1
fi

echo "Port 5432 is free. Continuing"

echo "Cleaning containers and volumes"
docker compose down -v --remove-orphans
docker volume prune -f

echo "Rebuilding Docker images"
docker compose build --no-cache

echo "Starting DB and API services in background"
docker compose up -d db web

echo "Seeding public holidays data"
docker compose run --rm seed

echo "Applying chmod to run and stop scripts"
chmod +x 03-run.sh
chmod +x 02-stop.sh
chmod +x 04-cleanup.sh

echo "Starting services"
echo "You can now access the API at http://localhost:8000"