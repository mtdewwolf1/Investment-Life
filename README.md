# Stock and Cryptocurrency Data Fetcher

This Python script fetches historical daily data for a predefined list of stock symbols and cryptocurrencies from the Alpha Vantage API, applying an internal rate limit to adhere to API constraints. The data is saved in JSON format, making it easy for further analysis, visualization, or integration into investment simulation games or other financial applications.

## Features

- Fetches daily historical data for stocks and cryptocurrencies.
- Saves data in structured JSON format.
- Implements an internal rate limiter to manage API usage.
- Customizable list of assets to fetch data for.
- Easy setup with `.env` file for API keys.

## Prerequisites

Before you run this script, you will need:

- Python 3.6 or higher.
- `requests` library.
- An API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).
- A `.env` file in the project root with your Alpha Vantage API key as `ALPHAAVANTAGE_API=<your_api_key>`.

## Installation

1. Clone this repository or download the script directly.
2. Install required Python packages:
    pip install requests python-dotenv


## Usage

To run the script and fetch data for the predefined symbols:

1. Navigate to the script's directory.
2. Run the script using Python:
    python data.py



The script will start fetching data for each symbol and save it in the `data` directory as JSON files, one per symbol.

## Customization

You can customize the list of stock symbols and cryptocurrencies by editing the `stock_symbols` and `crypto_symbols` lists in the script. Additionally, you can adjust the `start_year` and `start_month` in the `main` function to set the starting point for the data fetching.

## Rate Limiting

The script includes a `RateLimiter` class to ensure the number of API requests does not exceed 200 calls per minute, as per Alpha Vantage's guidelines. Adjust the `max_calls` and `period` parameters in the `RateLimiter` instantiation if your API plan allows different limits.

## Contributing

Contributions to improve the script or add new features are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).

