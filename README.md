# Binance Futures Testnet Trading Bot

A simple command-line trading bot built in Python for placing simulated trades on the Binance Futures Testnet.

## Features
* **Futures Trading**: Places USDT-M orders (Market, Limit).
* **Logging**: All API requests and responses are saved to `trading_bot.log`.
* **Structured Code**: Separates API interaction (`bot/client.py`) from the CLI interface (`cli.py`).

## Setup Instructions

1. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Credentials**
   * Create a copy of `.env.example` and name it `.env`.
   * Add your Testnet API Key and Secret:
     ```env
     BINANCE_API_KEY=your_testnet_api_key
     BINANCE_API_SECRET=your_testnet_api_secret
     ```

## How to Run Examples

There are two ways to use the bot:

### 1. Interactive Wizard (Bonus Feature)
Simply run the script with no arguments. It will display an interactive menu, ask you for inputs step-by-step, and handle any validation errors!
```bash
python cli.py
```

### 2. Command-Line Arguments (Advanced)
You can still place orders directly in one line:

**MARKET Order:**
```bash
python cli.py BTCUSDT BUY MARKET 0.01
```

**LIMIT Order:**
```bash
python cli.py BTCUSDT SELL LIMIT 0.01 --price 80000
```

### Get Help
```bash
python cli.py --help
```

## Logs
All API interactions and errors are automatically logged to `trading_bot.log`.

## Assumptions

* The user has an active Binance Futures Testnet account with a funded USDT-M wallet (via the testnet faucet). The bot does not check or top up balance itself, so orders may be rejected with a "Margin is insufficient" error if the wallet balance is too low for the requested quantity/leverage.
* Only `MARKET` and `LIMIT` order types are supported, as required by the task. `LIMIT` orders are placed with `timeInForce=GTC` (Good-Til-Canceled) by default.
* Quantity and price are accepted as entered and are not rounded or validated against a symbol's exchange-defined step size / tick size (e.g. Binance's `LOT_SIZE` / `PRICE_FILTER` rules). If a value doesn't match the symbol's precision rules, the API itself will reject the order.
* The symbol is not validated against Binance's list of tradable symbols before submission — an invalid symbol (e.g. a typo) will surface as an API error rather than a local validation error.
* `avgPrice` and `executedQty` will show as `0.00` / `0.0000` for LIMIT orders that don't fill immediately (status `NEW`), since they haven't executed yet. This is expected Binance API behavior, not a bug.
* Credentials are read from environment variables (via `.env` + `python-dotenv`) rather than passed on the command line, to avoid exposing API keys in shell history or process lists.
* ## Future Enhancements

With more time, the following would be natural next steps:

* **Exchange-info-based validation** — call `futures_exchange_info()` to validate quantity/price against each symbol's actual `LOT_SIZE` and `PRICE_FILTER` rules before submitting, instead of relying on the API to reject bad values.
* **Pre-trade balance/margin check** — call `futures_account_balance()` before submission and warn the user if the order's notional value clearly exceeds available margin, rather than only finding out from an API error.
* **Retry logic with backoff** — automatically retry on transient network failures (timeouts, connection resets) instead of failing on the first attempt.
* **Additional order types** — Stop-Limit and OCO orders would extend `place_order` naturally, since Binance's API just adds a `stopPrice` parameter to the same endpoint.
* **Automated test suite** — unit tests for the validation and payload-building logic in `client.py`, using a mocked Binance client so no real API calls are needed to run CI.
* **Order history / persistence** — store submitted orders locally (SQLite) so past orders can be listed or looked up without re-reading the log file.
* **Web-based UI** — a lightweight front end (e.g., Flask or Django) that reuses the same `BinanceBot` client class as the CLI, giving a browser-based way to place orders and view order history."# Trading-Bot" 
