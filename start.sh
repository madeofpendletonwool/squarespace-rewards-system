#!/bin/sh


# Create the Caddyfile
cat <<EOF > /app/Caddyfile
${DOMAIN_NAME} {
    reverse_proxy localhost:8080
}
EOF

# Debug: Output the Caddyfile to the log
cat /app/Caddyfile

# Start crond in background
crond -f -l 8 &

# Start Caddy in the background using the modified Caddyfile in /app
caddy run --config /app/Caddyfile &

# Start the FastAPI application
uvicorn backend-query:app --host 0.0.0.0 --port 8080
