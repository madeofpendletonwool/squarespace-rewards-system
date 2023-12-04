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

    # Open or create a separate sheet for processed order IDs
    try:
        processed_orders_sheet = client.open(google_sheet_name).worksheet("Processed Orders")
    except gspread.exceptions.WorksheetNotFound:
        processed_orders_sheet = client.open(google_sheet_name).add_worksheet(title="Processed Orders", rows="1000", cols="2")
        processed_orders_sheet.update('A1:B1', [['Order ID', 'Processed On']])

    # Fetch all rows as a list of lists from the main sheet
    all_rows = sheet.get_values()
    if len(all_rows) > 1:  # Check if there are more rows beyond the header
        header = all_rows[0]
        data_rows = all_rows[1:]
        existing_data = [dict(zip(header, row)) for row in data_rows]
        existing_emails = {row['Customer Email']: row for row in existing_data if 'Customer Email' in row}
    else:
        existing_data = []
        existing_emails = {}

    # Fetch processed order IDs from the separate sheet
    processed_order_ids = set(row[0] for row in processed_orders_sheet.get_all_values()[1:])  # Skip header row

    for order in orders:
        order_id = order['id']
        if order_id in processed_order_ids:
            continue  # Skip this order if it's already been processed

        customer_email = order.get('customerEmail', '')
        customer_name = f"{order['billingAddress']['firstName']} {order['billingAddress']['lastName']}"
        credits_earned = float(order['grandTotal']['value']) * 100  # Convert dollars to cents

        if customer_email in existing_emails:
            # Customer exists, update their credits
            row_index = existing_emails[customer_email]
            existing_credits = sheet.cell(row_index, 4).value  # Assuming Credits Earned is in column D
            existing_credits = float(existing_credits) if existing_credits else 0
            new_credits_earned = existing_credits + credits_earned

            # Update the Google Sheet with the new values
            sheet.update(f'D{row_index}', new_credits_earned)  # Update Credits Earned in column D
            sheet.update(f'F{row_index}', new_credits_earned)  # Update Net Credits in column F
        else:
            # New customer, add their information
            row_index = len(all_rows) + 2  # Calculate the new row index
            order_data = [customer_email, customer_name, credits_earned, "", credits_earned]
            sheet.insert_row(order_data, row_index)
            existing_emails[customer_email] = row_index  # Update the existing_emails dictionary

        # Record the processed order ID in the separate sheet
        processed_orders_sheet.append_row([order_id, str(datetime.datetime.now())])
        processed_order_ids.add(order_id)


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
