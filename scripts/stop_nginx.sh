#!/bin/bash

cd "$(dirname "$0")/.."

NGINX_CONF="$(pwd)/config/nginx/robah.conf"
NGINX_ROOT="$(pwd)"

if ! command -v nginx >/dev/null 2>&1; then
    echo "Nginx not found in PATH."
    exit 1
fi

nginx -s quit -c "$NGINX_CONF" -p "$NGINX_ROOT"
