import time
import pandas as pd
from selenium import webdriver
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


class Scraper:
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def open_website(self):
        try:
            self.driver.get(self.url)
            print(f"Website opened: {self.url}")
        except Exception as e:
            print(f"Error opening website: {e}")
            self.driver.quit()

    def scrape_data(self):
        data = {}
        try:
            for _ in range(10):  # Retry up to 10 times if elements are stale
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, '.marquee-item')
                    if not elements:
                        time.sleep(2)
                        continue
                    
                    for elem in elements:
                        text = elem.text.strip()

                        # Check for the relevant data and store it in the dictionary
                        if "22k Gold" in text:
                            data["22k Gold"] = text.split('₹')[-1].strip()
                        elif "Silver" in text:
                            data["Silver"] = text.split('₹')[-1].strip()
                        elif "Petrol" in text:
                            data["Petrol"] = text.split('₹')[-1].strip()
                        elif "Diesel" in text:
                            data["Diesel"] = text.split('₹')[-1].strip()
                        elif "Crude Oil" in text:
                            data["Crude Oil"] = text.split('$')[-1].strip()
                        elif "USD" in text:
                            data["USD"] = text.split('₹')[-1].strip()
                            break  # Exit the retry loop if scraping is successful
                    break  # Successful scraping, exit loop
                except StaleElementReferenceException:
                    print("Element became stale. Retrying...")
                    time.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"Error during scraping: {e}")

        return data

    def save_to_excel(self, data):
        try:
            df = pd.DataFrame([data])

            # Use openpyxl to handle Excel file properly
            if pd.io.common.file_exists(self.file_path):
                # File exists, so append data
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, index=False, header=False, sheet_name='Sheet1')
            else:
                # File doesn't exist, create new one and write the data
                df.to_excel(self.file_path, index=False)
            
            print(f"Data saved successfully to {self.file_path}")
        except Exception as e:
            print(f"Error saving data to Excel: {e}")

    def close_driver(self):
        try:
            self.driver.quit()
            print("Driver closed successfully.")
        except Exception as e:
            print(f"Error closing driver: {e}")


class Visualizer:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        # Load the data from the Excel file
        data = pd.read_excel(self.file_path)
        return data

    def generate_synthetic_dates(self):
        # Create a list of 6 synthetic dates (latest 6 days)
        today = datetime.today()
        dates = [today - timedelta(days=i) for i in range(6)]
        return dates

    def plot_data(self, data):
        # Generate synthetic dates
        dates = self.generate_synthetic_dates()

        # Check if the data has enough rows
        if len(data) != len(dates):
            raise ValueError(f"Data length ({len(data)}) does not match dates length ({len(dates)})")

        # Add the synthetic dates as a new column to the DataFrame
        data['Date'] = dates

        # Plot the data
        plt.figure(figsize=(10, 6))

        plt.subplot(2, 3, 1)
        plt.plot(data['Date'], data['22k Gold'], marker='o', color='gold', label="22k Gold")
        plt.title("22k Gold")
        plt.xlabel("Date")
        plt.ylabel("Price (₹/gm)")

        plt.subplot(2, 3, 2)
        plt.plot(data['Date'], data['Silver'], marker='o', color='silver', label="Silver")
        plt.title("Silver")
        plt.xlabel("Date")
        plt.ylabel("Price (₹/kg)")

        plt.subplot(2, 3, 3)
        plt.plot(data['Date'], data['Petrol'], marker='o', color='blue', label="Petrol")
        plt.title("Petrol")
        plt.xlabel("Date")
        plt.ylabel("Price (₹/L)")

        plt.subplot(2, 3, 4)
        plt.plot(data['Date'], data['Diesel'], marker='o', color='green', label="Diesel")
        plt.title("Diesel")
        plt.xlabel("Date")
        plt.ylabel("Price (₹/L)")

        plt.subplot(2, 3, 5)
        plt.plot(data['Date'], data['Crude Oil'], marker='o', color='brown', label="Crude Oil")
        plt.title("Crude Oil")
        plt.xlabel("Date")
        plt.ylabel("Price ($/barrel)")

        plt.subplot(2, 3, 6)
        plt.plot(data['Date'], data['USD'], marker='o', color='red', label="USD")
        plt.title("USD")
        plt.xlabel("Date")
        plt.ylabel("Price (₹)")

        plt.tight_layout()
        plt.show()

    def generate_visualization(self):
        # Load the data
        data = self.load_data()

        # Plot the data
        self.plot_data(data)

# Usage
url = "https://www.goodreturns.in/gold-rates/"
file_path = "scraped_data.xlsx"

# Uncomment the lines below to scrape data and save to Excel
# scraper = Scraper(url, file_path)
# scraper.open_website()
# data = scraper.scrape_data()
# if data:  # If data is successfully scraped
#     scraper.save_to_excel(data)
# scraper.close_driver()

visualizer = Visualizer(file_path)
visualizer.generate_visualization()
