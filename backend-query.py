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

google_sheet_name = os.environ.get('GOOGLE_SHEET_NAME')

# Decode the base64 string
encoded_credentials = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
decoded_credentials = base64.b64decode(encoded_credentials)

# Load the credentials as a JSON object
credentials_json = json.loads(decoded_credentials)

SECRET_KEY = os.environ.get("SECRET_KEY", "DL8ssxZ6EAWEGk")

# Google Sheets setup
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
client = gspread.authorize(creds)

@app.post("/get-credits")
async def get_credits(request: Request):
    data = await request.json()

    # Verify secret key
    if data.get("secret_key") != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    email = data.get("email")

    # Access Google Sheets
    try:
        # Assuming you have set up credentials and client as a global variable
        sheet = client.open(google_sheet_name).sheet1

        # Find the row with the requested email
        cell = sheet.find(email)
        if cell:
            # Fetch the row data
            row = sheet.row_values(cell.row)
            # Assuming credits are in the 3rd column (index 2)
            credit_count = float(row[2]) if row[2] else 0
        else:
            # User not found
            credit_count = 0

    except Exception as e:
        # Handle exceptions, e.g., if sheet not found
        print(f"Error accessing Google Sheets: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"credits": credit_count}

# Run the server (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
