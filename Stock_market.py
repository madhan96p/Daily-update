import requests
import pandas as pd
from datetime import datetime, timedelta

class Gold:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.goldapi.io/api/XAU/INR"
        self.headers = {
            "x-access-token": self.api_key,
            "Content-Type": "application/json"
        }

    def fetch_gold_prices(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            timestamp_unix = data['timestamp']
            timestamp_human_readable = datetime.utcfromtimestamp(timestamp_unix).strftime('%Y-%m-%d %H:%M:%S')
            prices = {
                "Timestamp": timestamp_human_readable,
                "24K Price (INR/g)": data['price_gram_24k'],
                "22K Price (INR/g)": data['price_gram_22k'],
                "18K Price (INR/g)": data['price_gram_18k']
            }
            return prices
        except requests.exceptions.RequestException as e:
            print(f"Error fetching gold data: {e}")
            return None


class Stock:
    def __init__(self, api_key, symbol):
        self.api_key = api_key
        self.symbol = symbol
        self.url = "https://finnhub.io/api/v1/quote"

    def fetch_stock_data(self, usd_to_inr=83.0):
        try:
            params = {"symbol": self.symbol, "token": self.api_key}
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()

            utc_timestamp = datetime.utcfromtimestamp(data['t'])
            ist_timestamp = utc_timestamp + timedelta(hours=5, minutes=30)

            stock_data = {
                "Timestamp (UTC)": utc_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "Timestamp (IST)": ist_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "Current Price (USD)": data['c'],
                "Current Price (INR)": round(data['c'] * usd_to_inr, 2),
                "Price Change (INR)": round(data['d'] * usd_to_inr, 2),
                "Percentage Change (%)": round(data['dp'], 2),
                "High Price (INR)": round(data['h'] * usd_to_inr, 2),
                "Low Price (INR)": round(data['l'] * usd_to_inr, 2),
                "Open Price (INR)": round(data['o'] * usd_to_inr, 2),
                "Previous Close (INR)": round(data['pc'] * usd_to_inr, 2)
            }
            return stock_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock data: {e}")
            return None


def save_to_excel(data_dict, sheet_name, file_path="market_data.xlsx"):
    if data_dict:
        df = pd.DataFrame([data_dict])
        try:
            with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                if sheet_name in writer.sheets:
                    startrow = writer.sheets[sheet_name].max_row
                    df.to_excel(writer, index=False, header=False, sheet_name=sheet_name, startrow=startrow)
               
                else:
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
            print(f"Data saved to sheet '{sheet_name}' in {file_path}.")

        except FileNotFoundError:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
            print(f"Excel file created and data saved to sheet '{sheet_name}'.")



if __name__ == "__main__":

    def gold():
        gold_api_key = "goldapi-oxeiosm5awdx8x-io"
        gold_obj = Gold(gold_api_key)
        gold_prices = gold_obj.fetch_gold_prices()
        if gold_prices:
            print("Gold Prices:", gold_prices)
            save_to_excel(gold_prices, sheet_name="Gold Prices")

    def Apple_stock():
        stock_api_key = "ctpajl9r01qqsrsacaj0ctpajl9r01qqsrsacajg"
        apple_stock = Stock(stock_api_key, "AAPL")
        apple_data = apple_stock.fetch_stock_data()
        if apple_data:
            print("Apple Stock Data:")
            for key, value in apple_data.items():
                print(f"{key}: {value}")
            save_to_excel(apple_data, sheet_name="Apple Stock")

    user_input = input("Enter 'gold' or 'stock' to fetch data: ")

    if user_input.lower() == "gold":
        gold()
    elif user_input.lower() == "stock":
        Apple_stock()