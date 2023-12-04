# Start from the official Caddy image
FROM caddy:latest

# Set working directory in the container
WORKDIR /app

# Install Python and other dependencies
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache openrc

# Copy the Python requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Python scripts into the container at /app
COPY order-submit.py backend-query.py /app/

# Add crontab file in the cron directory
COPY order-submit-cron /etc/crontabs/root

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Copy your Caddyfile and startup script into the container
COPY Caddyfile start.sh /app/

# Make the startup script executable
RUN chmod +x /app/start.sh

# The command to run the startup script
CMD ["/app/start.sh"]
