import os
import time
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ALPHAAVANTAGE_API")

# Ensure this path exists or is correctly specified according to your environment
save_directory = "C:/Users/mtdew/Projects/pygame_projects/Investment Life/data"

# Stock symbols
stock_symbols = [
    "MDVN", "AAPL", "UVE", "AMZN", "REGN",
    "PCLN", "NFLX", "ILMN", "ALXN", "NEU",
    "BSTC", "MNST", "NVDA"
]

# Cryptocurrency symbols
crypto_symbols = [
    "BTC", "ETH", "BNB", "XRP", "ADA",
    "SOL", "DOGE", "DOT", "AVAX", "LINK",
    "LTC", "UNI", "LUNA", "BCH", "XLM",
    "MANA", "ALGO", "VET", "ATOM", "FIL"
]


class RateLimiter:
    def __init__(self, max_calls, period=60):
        self.max_calls = max_calls
        self.period = period
        self.timestamps = []

    def wait(self):
        now = time.time()
        while self.timestamps and now - self.timestamps[0] > self.period:
            self.timestamps.pop(0)
        if len(self.timestamps) >= self.max_calls:
            sleep_time = self.period - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.timestamps.append(time.time())


rate_limiter = RateLimiter(max_calls=200, period=60)
rate_limiter_error = "You have exceeded the API speed limit. Please wait a minute and try again."


def fetch_stock_data(symbol, start_year, start_month):
    rate_limiter.wait()
    start_date = f"{start_year}-{start_month:02d}-01"
    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize"
           f"=full")

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})
        prices = {date: price_data["4. close"] for date, price_data in time_series.items() if date >= start_date}
        return prices
    else:
        print(f"Failed to fetch data for {symbol}")
        return {}


def fetch_crypto_data(symbol, start_year, start_month):
    rate_limiter.wait()
    start_date = f"{start_year}-{start_month:02d}-01"
    url = (f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey="
           f"{API_KEY}&outputsize=full")

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("Time Series (Digital Currency Daily)", {})
        prices = {date: price_data["4a. close (USD)"] for date, price_data in time_series.items() if date >= start_date}
        return prices
    else:
        print(f"Failed to fetch data for {symbol}")
        return {}


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_data_to_file(symbol, data, is_crypto=False):
    # Determine the type of asset and adjust the filename accordingly
    file_name = f"{symbol}.json"  # Change the file extension to .json
    file_path = os.path.join(save_directory, file_name)

    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)  # Save the data as JSON
        print(f"Data for {symbol} saved successfully as JSON.")
    except Exception as e:
        print(f"Failed to save data for {symbol} as JSON: {e}")


def main():
    ensure_directory_exists(save_directory)
    start_year = 2010
    start_month = 1

    for symbol in stock_symbols:
        stock_data = fetch_stock_data(symbol, start_year, start_month)
        save_data_to_file(symbol, stock_data)

    for symbol in crypto_symbols:
        crypto_data = fetch_crypto_data(symbol, start_year, start_month)
        save_data_to_file(symbol, crypto_data, is_crypto=True)



if __name__ == "__main__":
    main()
