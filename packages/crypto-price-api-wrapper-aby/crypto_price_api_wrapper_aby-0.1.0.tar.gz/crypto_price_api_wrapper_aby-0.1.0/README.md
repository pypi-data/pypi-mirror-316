Here’s a structured content for your `README.md` file. It will provide details about your Python package, how to install and use it, and other necessary information.

```markdown
# Crypto Price

A simple Python package to fetch live cryptocurrency prices using the CoinMarketCap API.

## Installation

To install the `crypto_price` package, you can use pip:

```bash
pip install crypto_price
```

## Requirements

- Python 3.x
- `requests` library (installed automatically with the package)

## Setup

1. First, you'll need to create an account on [CoinMarketCap](https://coinmarketcap.com/api/) and get your API key.
2. Once you have your API key, you can use it in your code to fetch cryptocurrency data.

## Usage

### Basic Example

Here's an example of how to use the `crypto_price` package to get the live price of Bitcoin (BTC) in USD:

```python
from crypto_price.crypto_price import CryptoPrice

# Initialize the CryptoPrice class with your CoinMarketCap API key
api_key = "YOUR_COINMARKETCAP_API_KEY"
crypto = CryptoPrice(api_key)

# Fetch the price of Bitcoin (BTC) in USD
btc_price = crypto.get_price("BTC", "USD")
print(f"The current price of BTC is {btc_price['price']} USD.")
```

### Fetching Prices for Multiple Cryptocurrencies

You can fetch prices for multiple cryptocurrencies at once:

```python
from crypto_price.crypto_price import CryptoPrice

api_key = "YOUR_COINMARKETCAP_API_KEY"
crypto = CryptoPrice(api_key)

# List of symbols you want to fetch the price for
symbols = ["BTC", "ETH", "XRP"]

# Fetch prices for all cryptocurrencies in INR
prices = crypto.get_prices(symbols, "INR")

for symbol, price_data in prices.items():
    print(f"The current price of {symbol} is {price_data['price']} INR.")
```

### API Wrapper Functions

- **get_price(symbol, convert)**: Fetches the latest price of a single cryptocurrency.  
   - `symbol`: The cryptocurrency symbol (e.g., 'BTC', 'ETH').
   - `convert`: The currency to convert to (default: USD).

- **get_prices(symbols, convert)**: Fetches the latest prices for multiple cryptocurrencies.  
   - `symbols`: List of cryptocurrency symbols (e.g., `['BTC', 'ETH']`).
   - `convert`: The currency to convert to (default: USD).

## Notes

- Ensure you use your own valid CoinMarketCap API key.
- The CoinMarketCap API may have rate limits, so please be mindful of the number of requests.
  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Key Sections:
1. **Installation**: Explains how to install the package using pip.
2. **Requirements**: Lists the Python version and dependencies.
3. **Usage**: Provides code examples for basic usage, fetching prices for multiple cryptocurrencies, and using the provided wrapper functions.
4. **API Functions**: Describes the available functions in the package.
5. **License**: Information about licensing (MIT license in this case).

---

This template covers the necessary details to help users understand how to set up and use your library. You can adjust it based on your specific implementation or if you have additional features.