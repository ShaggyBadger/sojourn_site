#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/compose.production.yaml"

usage() {
  cat <<'EOF'
Usage: ./view_logs.sh [app|crash|docker|path]

  app     Open Django warnings and errors in lnav (default)
  crash   Open Django errors in lnav
  docker  Follow container and Gunicorn output
  path    Print the host path containing the log files
EOF
}

command="${1:-app}"

case "$command" in
  app|crash|path)
    volume="$(docker volume ls \
      --filter label=com.docker.compose.volume=sojourn_logs \
      --format '{{.Name}}')"

    if [[ -z "$volume" ]]; then
      echo "Could not find the sojourn_logs Docker volume." >&2
      echo "Is the production service running?" >&2
      exit 1
    fi

    log_dir="$(docker volume inspect "$volume" --format '{{.Mountpoint}}')"

    if [[ "$command" == "path" ]]; then
      printf '%s\n' "$log_dir"
    elif [[ "$command" == "app" ]]; then
      sudo lnav "$log_dir/application.log"
    else
      sudo lnav "$log_dir/crash.log"
    fi
    ;;
  docker)
    exec docker compose -f "$COMPOSE_FILE" logs -f web
    ;;
  -h|--help)
    usage
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
