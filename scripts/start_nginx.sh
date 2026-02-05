#!/bin/bash

cd "$(dirname "$0")/.."

NGINX_CONF="$(pwd)/config/nginx/robah.conf"
NGINX_ROOT="$(pwd)"
NGINX_LOG_DIR="$(pwd)/logs/nginx"

if [[ ! -f "$NGINX_CONF" ]]; then
    echo "Nginx config not found: $NGINX_CONF"
    exit 1
fi

if ! command -v nginx >/dev/null 2>&1; then
    echo "Nginx not found in PATH. Install nginx and add it to PATH."
    exit 1
fi

mkdir -p "$NGINX_LOG_DIR"

nginx -s quit -c "$NGINX_CONF" -p "$NGINX_ROOT" >/dev/null 2>&1
nginx -c "$NGINX_CONF" -p "$NGINX_ROOT"
