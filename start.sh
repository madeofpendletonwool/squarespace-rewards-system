#!/bin/sh

# Replace DOMAIN_PLACEHOLDER with the actual domain from the environment variable
sed -i "s/DOMAIN_PLACEHOLDER/${DOMAIN_NAME}/g" /etc/caddy/Caddyfile

# Start crond in background
crond -f -l 8 &

# Start Caddy in the background
caddy run --config /etc/caddy/Caddyfile &

# Start the FastAPI application
uvicorn backend-query:app --host 0.0.0.0 --port 443
