from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import gspread
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

# Google Sheets setup
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Your Spreadsheet Name').sheet1

@app.post("/get-credits")
async def get_credits(request: Request):
    data = await request.json()
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
