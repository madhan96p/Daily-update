import requests
import pandas as pd
from datetime import datetime

# API Key and URL
api_key = "goldapi-oxeiosm5awdx8x-io"
url = "https://www.goldapi.io/api/XAU/INR"

# Headers
headers = {
    "x-access-token": api_key,
    "Content-Type": "application/json"
}

# Try fetching the data
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses
    data = response.json()

    # Convert the timestamp to a human-readable format
    timestamp_unix = data['timestamp']
    timestamp_human_readable = datetime.utcfromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M:%S')

    # Extract the required prices
    price_per_gram_24k = data['price_gram_24k']
    price_per_gram_22k = data['price_gram_22k']
    price_per_gram_18k = data['price_gram_18k']

    # Print the human-readable timestamp first
    print(f"Timestamp (Human-readable): {timestamp_human_readable}")
    print(f"Gold Price (per gram 24K in INR): ₹{price_per_gram_24k}")
    print(f"Gold Price (per gram 22K in INR): ₹{price_per_gram_22k}")
    print(f"Gold Price (per gram 18K in INR): ₹{price_per_gram_18k}")

    # Prepare the data for the DataFrame
    df_data = {
        'timestamp': [timestamp_human_readable],
        'price_gram_24k': [price_per_gram_24k],
        'price_gram_22k': [price_per_gram_22k],
        'price_gram_18k': [price_per_gram_18k]
    }

    # Create a DataFrame
    df = pd.DataFrame(df_data)

    # Define the Excel file path
    file_path = "gold_prices.xlsx"

    # Check if the Excel file exists, and if it does, append new data to it
    try:
        existing_df = pd.read_excel(file_path)  # Try to read the existing Excel file
        df.to_excel(file_path, index=False, header=False, mode='a')  # Append without writing the header
        print("Data appended to the existing Excel file.")
    except FileNotFoundError:
        df.to_excel(file_path, index=False)  # Create a new file if it doesn't exist
        print("Excel file created and data saved.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
