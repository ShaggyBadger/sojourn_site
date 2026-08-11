#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/compose.production.yaml"

echo "=== Restarting Sojourn production stack ==="

echo "[1/3] Rebuilding and restarting Docker service..."
docker compose -f "$COMPOSE_FILE" up --build -d

echo "[2/3] Checking container status..."
docker compose -f "$COMPOSE_FILE" ps

echo "[3/3] Recent application logs..."
docker compose -f "$COMPOSE_FILE" logs --tail=20 web

echo "=== Done ==="
