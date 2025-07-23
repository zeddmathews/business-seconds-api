#!/bin/bash
set -e

echo "Cleaning containers and volumes"
docker compose down -v