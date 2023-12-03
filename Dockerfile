# Use an official Python runtime as a parent image
FROM python:3.9.18-slim-bullseye

# Set the maintainer label
LABEL maintainer="collinp@collinpendleton.com"

# Set working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Assuming you have a requirements.txt file for your Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy the Python scripts into the container at /app
COPY order-submit.py /app/
COPY backend-query.py /app/

# Add crontab file in the cron directory
RUN echo "*/10 * * * * /usr/local/bin/python3 /app/order-submit.py >> /var/log/cron.log 2>&1" > /etc/cron.d/order-submit-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/order-submit-cron

# Apply cron job
RUN crontab /etc/cron.d/order-submit-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
# Start FastAPI application using Uvicorn
CMD cron && uvicorn backend-query:app --host 0.0.0.0 --port 443
