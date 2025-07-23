#!/bin/bash
set -e

echo "Starting containers..."
docker compose up -d db web

echo "Checking and seeding holidays if needed..."
docker compose run --rm seed

echo "All set!"