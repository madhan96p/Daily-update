from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException




# Setup WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# URLs for data (Replace with actual URLs)
gold_silver_url = "https://www.goldpriceindia.com/"
fuel_price_url = "https://www.mypetrolprice.com/"

# Data Dictionary to Store Results
data = {
    "Date": [],
    "Silver (₹/kg)": [],
    "Gold 22K (₹/g)": [],
    "Gold 24K (₹/g)": [],
    "Petrol (₹/L) (Highest)": [],
    "Diesel (₹/L) (Highest)": [],
    "Petrol (₹/L) (Lowest)": [],
    "Diesel (₹/L) (Lowest)": []
}

# Scrape Gold and Silver Prices
driver.get(gold_silver_url)
try:
    # Wait for the price table to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "price_table"))
    )
    gold_silver_table = driver.find_element(By.CLASS_NAME, "price_table")

    # Extract Gold and Silver Prices (Update with correct tags)
    rows = gold_silver_table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if "Silver" in row.text:
            data["Silver (₹/kg)"].append(float(cells[1].text.replace(",", "")) * 1000)
        if "Gold 22K" in row.text:
            data["Gold 22K (₹/g)"].append(float(cells[1].text.replace(",", "")))
        if "Gold 24K" in row.text:
            data["Gold 24K (₹/g)"].append(float(cells[1].text.replace(",", "")))

    # Scrape Fuel Prices
    driver.get(fuel_price_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "priceTable")))
    fuel_table = driver.find_element(By.ID, "priceTable")

    # Extract Fuel Prices (Update with correct tags)
    rows = fuel_table.find_elements(By.TAG_NAME, "tr")
    highest_petrol = 0
    lowest_petrol = float('inf')
    highest_diesel = 0
    lowest_diesel = float('inf')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        try:
            location = cells[0].text
            petrol_price = float(cells[1].text)
            diesel_price = float(cells[2].text)

            highest_petrol = max(highest_petrol, petrol_price)
            lowest_petrol = min(lowest_petrol, petrol_price)
            highest_diesel = max(highest_diesel, diesel_price)
            lowest_diesel = min(lowest_diesel, diesel_price)
        except:
            pass

    data["Petrol (₹/L) (Highest)"].append(highest_petrol)
    data["Diesel (₹/L) (Highest)"].append(highest_diesel)
    data["Petrol (₹/L) (Lowest)"].append(lowest_petrol)
    data["Diesel (₹/L) (Lowest)"].append(lowest_diesel)

    # Add Date
    from datetime import datetime
    data["Date"].append(datetime.today().strftime('%Y-%m-%d'))

except TimeoutException:
    print("Timeout: The element with CLASS_NAME 'price_table' was not found.")
    # Debugging: Take a screenshot of the page to verify
    driver.save_screenshot("debug_screenshot.png")
    print("Screenshot saved as 'debug_screenshot.png'. Check the file for debugging.")
    driver.quit()
    exit()

# Save Data to Excel
df = pd.DataFrame(data)
df.to_excel("commodity_prices.xlsx", index=False)
print("Data saved to commodity_prices.xlsx")