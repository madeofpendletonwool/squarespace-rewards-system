import requests
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import os
import base64
import json

# Decode the base64 string
encoded_credentials = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
decoded_credentials = base64.b64decode(encoded_credentials)
# Get Squarespace key
squarespace_api = os.environ.get('SQUARESPACE_API')

google_sheet_name = os.environ.get('GOOGLE_SHEET_NAME')


# Function to fetch orders from Squarespace
def fetch_orders(api_key, start_datetime, end_datetime):
    # Current time as the end datetime
    # end_datetime = datetime.datetime.utcnow().isoformat() + 'Z'

    url = f"https://api.squarespace.com/1.0/commerce/orders?modifiedAfter={start_datetime}&modifiedBefore={end_datetime}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'User-Agent': 'YOUR_CUSTOM_APP_DESCRIPTION'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['result']  # List of orders
    else:
        # Handle errors
        print(f"Error fetching orders: {response.status_code}")
        return []


# Function to update Google Sheets with the fetched orders
def update_google_sheet(orders):
    credentials_json = json.loads(decoded_credentials)
    print(orders)
    # Set up Google Sheets credentials and client
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet and the specific sheet
    sheet = client.open(google_sheet_name).sheet1

    # Fetch all existing data to check for duplicates and accumulate credits
    existing_data = sheet.get_all_records()
    existing_emails = {row['Customer Email']: row for row in existing_data}

    for order in orders:
        customer_email = order.get('customerEmail', '')
        customer_name = f"{order['billingAddress']['firstName']} {order['billingAddress']['lastName']}"
        credits_earned = float(order['grandTotal']['value']) * 100  # Convert dollars to cents

        if customer_email in existing_emails:
            # Customer exists, update their credits
            existing_row = existing_emails[customer_email]
            row_index = existing_data.index(existing_row) + 2  # +2 due to Google Sheets indexing
            new_credits_earned = existing_row['Credits Earned'] + credits_earned
            sheet.update(f'C{row_index}', new_credits_earned)  # Update Credits Earned in column C
            sheet.update(f'E{row_index}', new_credits_earned)  # Update Net Credits in column E
        else:
            # New customer, add their information
            order_data = [customer_email, customer_name, credits_earned, "", credits_earned]
            sheet.append_row(order_data)


# Main function to run the scheduled job
def main():
    api_key = squarespace_api
    # Define your time range for fetching orders
    start_datetime = '2000-01-01T00:00:00Z'  # Adjust as needed
    end_datetime = datetime.datetime.utcnow().isoformat() + 'Z'

    orders = fetch_orders(api_key, start_datetime, end_datetime)
    if orders:
        update_google_sheet(orders)


if __name__ == "__main__":
    main()
