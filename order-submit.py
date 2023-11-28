import requests
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys

squarespace_api = sys.argv[1]
google_json_file = sys.argv[2]
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
    print(orders)
    # Set up Google Sheets credentials and client
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_json_file, scope)
    client = gspread.authorize(creds)

    # Open the spreadsheet and the specific sheet
    sheet = client.open('TestCookiesData').sheet1

    customer_id_counter = 1  # If you're generating Customer IDs
    for order in orders:
        # Extracting Customer Name
        customer_name = f"{order['billingAddress']['firstName']} {order['billingAddress']['lastName']}"

        # Generating a simple Customer ID (or use a more sophisticated method if preferred)
        customer_id = f"CUST{customer_id_counter}"
        customer_id_counter += 1

        # Calculating Credits Earned (assuming grandTotal is a string of a float value)
        credits_earned = float(order['grandTotal']['value']) * 100  # Convert dollars to cents

        # Preparing the row data
        order_data = [customer_id, customer_name, credits_earned, "", credits_earned]  # Leave Credits Spent blank for now

        # Append the row to the sheet
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
