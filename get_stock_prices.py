import csv
import requests
import json
from datetime import datetime

print("🌟 HK Stock Price Tracker Starting...")

# Read stock codes from CSV file
stocks = []
try:
    with open('hk_stocks.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            if row and row[0].strip():
                code = row[0].strip().zfill(4)   # Ensure 4 digits
                stocks.append({
                    'code': code,
                    'full_code': f"{code}.HK"
                })
except FileNotFoundError:
    print("❌ Error: hk_stocks.csv file not found!")
    exit()

print(f"📊 Found {len(stocks)} stocks to track!")

# Timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S HKT")
results = [f"Stock Price Report - {timestamp}", "-" * 50]

# Headers to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

for stock in stocks:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock['full_code']}"
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()   # Raise error if not 200
        
        data = response.json()

        # Extract current price safely
        result = data.get('chart', {}).get('result')
        if result and len(result) > 0:
            meta = result[0].get('meta', {})
            price = meta.get('regularMarketPrice') or meta.get('previousClose')
            
            if price:
                result_line = f"{stock['code']}: HK${price:.2f}"
                print(f"✅ {result_line}")
                results.append(result_line)
            else:
                raise ValueError("Price not found in data")
        else:
            raise ValueError("No result in API response")

    except Exception as e:
        error_msg = f"{stock['code']}: Price not available (Error)"
        print(f"❌ {error_msg}")
        results.append(error_msg)

# Save results to text file
with open('latest_prices.txt', 'w', encoding='utf-8') as file:
    for line in results:
        file.write(line + '\n')

print("\n✅ Done! Check 'latest_prices.txt' for the latest stock prices.")
print(f"   Report generated at: {timestamp}")
