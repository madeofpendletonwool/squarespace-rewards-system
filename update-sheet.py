import gspread
from oauth2client.service_account import ServiceAccountCredentials


def update_google_sheet(order_data):
    # Google Sheets credentials
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet and the specific sheet
    sheet = client.open('Your Spreadsheet Name').sheet1

    # Add the order data
    # Assuming order_data is a dictionary containing the relevant information
    sheet.append_row([order_data['orderId'], order_data['customerName'], order_data['creditsEarned'], ...])
