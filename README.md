# Binance Futures Trading Bot (Testnet)

A simplified Python trading bot for Binance Futures Testnet (USDT-M), supporting Market, Limit, and Trailing Stop Market orders with a clean, modular structure.

## Features
- **Order Types**: MARKET, LIMIT, and TRAILING_STOP_MARKET (Bonus).
- **Sides**: BUY and SELL.
- **CLI Modes**: 
  - **Direct**: Supply arguments via command line.
  - **Interactive**: Run without arguments for a guided prompt.
- **Robust Logging**: Separate logs for Market and Limit (including Trailing) orders in the `logs/` directory.
- **Error Handling**: Validates user input and handles Binance API/Network errors gracefully.

## Prerequisites
- Python 3.x
- Binance Futures Testnet API Key & Secret.

## Setup
1.  **Clone the repository**.
2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/Scripts/activate  # Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables**:
    Create a `.env` file in the `trading_bot/` directory (see `.env.example`):
    ```env
    BINANCE_TESTNET_API_KEY=your_api_key_here
    BINANCE_TESTNET_API_SECRET=your_api_secret_here
    ```

## Usage

### 1. Interactive Mode
Simply run the script without arguments:
```bash
python cli.py
```

### 2. Market Order Example
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
```

### 3. Limit Order Example
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 100000
```

### 4. Trailing Stop Market Example (Bonus)
```bash
python cli.py --symbol BTCUSDT --side BUY --type TRAILING_STOP_MARKET --qty 0.01 --callback_rate 1.0
```

## Logs
Logs are stored in the `logs/` directory:
- `market_order.log`: Contains records of Market and Trailing Stop Market requests/responses.
- `limit_order.log`: Contains records of Limit order requests/responses.

## Assumptions & Design
- **API Version**: Uses Binance Futures API v1 (`/fapi/v1`).
- **Signing**: Implements HMAC-SHA256 and Ed25519 signing (automatically detects Ed25519 if secret looks like a private key).
- **Parameters**: All parameters are passed in the query string for signed requests as per Binance best practices for Python `requests` implementations.
