#!/bin/bash

# Google json key
export GOOGLE_CREDENTIALS_BASE64='your_base64_encoded_string_here'
# Secret key to access the credit count info
export SECRET_KEY=''
# Squarespace key to access order info
export SQUARESPACE_API=''
# Google Sheet Name
export GOOGLE_SHEET_NAME=''

# Update and upgrade the server
apt-get update -y && apt-get upgrade -y

# Install Docker
# Add Docker's official GPG key:
apt-get update
apt-get install ca-certificates curl gnupg -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg |  gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update

# Install docker
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Start Docker and enable it to run on boot
systemctl start docker
systemctl enable docker

# Pull your Docker image from Docker Hub
# Replace 'your_docker_image' with your actual Docker image name
docker pull madeofpendletonwool/squarespace-sheet-updater:latest

# Run your Docker container
# Make sure to replace 'your_docker_image' and set any necessary environment variables
docker run -d --name squarespace-sheet-updater -p 80:80 \
-e GOOGLE_CREDENTIALS_BASE64="$GOOGLE_CREDENTIALS_BASE64" \
-e SECRET_KEY="$SECRET_KEY" \
-e SQUARESPACE_API="$SQUARESPACE_API" \
-e GOOGLE_SHEET_NAME="$GOOGLE_SHEET_NAME" \
madeofpendletonwool/squarespace-sheet-updater:latest
