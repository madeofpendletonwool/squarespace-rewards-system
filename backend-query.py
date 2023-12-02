from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from google.oauth2.service_account import Credentials
import gspread
import os
import base64
import json
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Decode the base64 string
encoded_credentials = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
decoded_credentials = base64.b64decode(encoded_credentials)

# Load the credentials as a JSON object
credentials_json = json.loads(decoded_credentials)

SECRET_KEY = os.environ.get("SECRET_KEY", "DL8ssxZ6EAWEGk")

# Google Sheets setup
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(credentials_json)
client = gspread.authorize(creds)
sheet = client.open('Your Spreadsheet Name').sheet1

@app.post("/get-credits")
async def get_credits(request: Request):
    data = await request.json()

    # Verify secret key
    if data.get("secret_key") != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    name = data.get("name")
    email = data.get("email")



    # Search for the user in the Google Sheet
    # Implement the logic to search the sheet and calculate the credits
    # ...

    # Placeholder response
    credits = 100  # Replace with actual logic to calculate credits

    return {"credits": credits}

# Run the server (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
