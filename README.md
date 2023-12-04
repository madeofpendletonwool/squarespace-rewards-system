# squarespace-rewards-system
 A rewards system for squarespace stores that creates points per dollar spent


## Installation

To use, dump this information into the user-data of linode as you kick off the server

Ensure you replace the environment vars at the top:
GOOGLE_CREDENTIALS_BASE64: 
SECRET_KEY: 
SQUARESPACE_API: 
GOOGLE_SHEET_NAME: 
DOMAIN_NAME:

```#!/bin/bash
# Google json key
export GOOGLE_CREDENTIALS_BASE64='your_base64_encoded_string_here'
# Secret key to access the credit count info
export SECRET_KEY=''
# Squarespace key to access order info
export SQUARESPACE_API=''
# Google Sheet Name
export GOOGLE_SHEET_NAME=''
# Domain Name for Squarespace
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
docker run -d --name squarespace-sheet-updater -p 443:443 \
-e GOOGLE_CREDENTIALS_BASE64="$GOOGLE_CREDENTIALS_BASE64" \
-e SECRET_KEY="$SECRET_KEY" \
-e SQUARESPACE_API="$SQUARESPACE_API" \
-e GOOGLE_SHEET_NAME="$GOOGLE_SHEET_NAME" \
-e DOMAIN_NAME="$DOMAIN_NAME" \
madeofpendletonwool/squarespace-sheet-updater:latest
```

Make requests like this:

```
curl -X POST http://linode-ip:80/get-credits -H "Content-Type: application/json" -d '{"name": "Test Name", "email": "test@example.com", "secret_key": "your-secret-key"}'
```


Below is the code for the javascript form to pull credits from the linode server ensure you update the secret_key with the one input into the linode server and the linode server ip.

```html
<form id="creditQueryForm">
    <input type="text" id="name" placeholder="Name">
    <input type="email" id="email" placeholder="Email">
    <button type="submit">Check Credits</button>
</form>
<div id="result"></div>

<script>
    document.getElementById('creditQueryForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const secret_key = 'your-secret-key';
        const api_endpoint = 'https://your-linode-server:443/get-credits';  // Adjust with your actual API endpoint

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;

        fetch(api_endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                secret_key: secret_key  // Include the secret key in the request
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('result').textContent = 'Credits: ' + data.credits;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').textContent = 'Error: ' + error.message;
        });
    });
</script>

```