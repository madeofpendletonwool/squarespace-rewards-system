#!/bin/bash

# Update and upgrade the server
apt-get update -y && apt-get upgrade -y

# Install Docker
apt-get install docker.io -y

# Start Docker and enable it to run on boot
systemctl start docker
systemctl enable docker

# Create a directory for your application and credentials
mkdir /app
cd /app

# (Optional) Download your Google credentials JSON file
# Make sure to securely transfer this file to your server
# For example, using `scp` or a secure file transfer service
# wget 'url_to_your_google_credentials_json' -O /app/your_credentials.json

# Pull your Docker image from Docker Hub
# Replace 'your_docker_image' with your actual Docker image name
docker pull your_docker_image

# Run your Docker container
# Make sure to replace 'your_docker_image' and set any necessary environment variables
docker run -d --name your_app_container -p 80:80 your_docker_image
