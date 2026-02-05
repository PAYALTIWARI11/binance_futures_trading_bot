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
## Configuration
1.  **Environment Setup**: Create a `.env` file from the [template](.env.example):
    ```env
    BINANCE_ENV=testnet # or production
    
    # Testnet
    BINANCE_TESTNET_API_KEY=...
    BINANCE_TESTNET_API_SECRET=...
    
    # Production
    BINANCE_API_KEY=...
    BINANCE_API_SECRET=...
    ```

## Usage

### 1. Local Python Execution
```bash
python cli.py
```

### 2. Docker Execution (Recommended for Deployment)
Build the image:
```bash
docker build -t binance-bot .
```
Run interactively:
```bash
docker run -it --env-file .env binance-bot
```

## Logs
Logs are stored in the `logs/` directory. For Docker:
```bash
docker run -it --env-file .env -v ${PWD}/logs:/app/logs binance-bot
```


## Assumptions & Design
- **API Version**: Uses Binance Futures API v1 (`/fapi/v1`).
- **Signing**: Implements HMAC-SHA256 and Ed25519 signing (automatically detects Ed25519 if secret looks like a private key).
- **Parameters**: All parameters are passed in the query string for signed requests as per Binance best practices for Python `requests` implementations.
