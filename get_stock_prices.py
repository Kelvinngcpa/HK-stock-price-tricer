import csv
import requests
import json
from datetime import datetime

print("🌟 HK Stock Price Tracker Starting...")

# Read stock codes from CSV file
stocks = []
with open('hk_stocks.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        if row:  # Make sure row is not empty
            stock_code = row[0]
            # Format HK stock code (add .HK for the API)
            stocks.append({
                'code': stock_code,
                'full_code': stock_code + '.HK'
            })

print(f"📊 Found {len(stocks)} stocks to track!")

# Create a result file with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
results = []
results.append(f"Stock Price Report - {timestamp}")
results.append("-" * 40)

# For each stock, try to get its price
for stock in stocks:
    try:
        # Using a free stock API (Yahoo Finance)
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock['full_code']}"
        response = requests.get(url)
        data = response.json()
        
        # Extract the price (this is like finding treasure in a map!)
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        
        result = f"{stock['code']}: HK${price:.2f}"
        print(f"✅ {result}")
        results.append(result)
        
    except Exception as e:
        error_msg = f"{stock['code']}: Price not available"
        print(f"❌ {error_msg}")
        results.append(error_msg)

# Save all results to a file
with open('latest_prices.txt', 'w') as file:
    for line in results:
        file.write(line + '\n')

print("✅ Done! Check latest_prices.txt for your stock prices!")
