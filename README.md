# Binance Futures Trading Bot (Testnet)

A professional command-line interface (CLI) application built in Python to interact with the **Binance Futures Testnet (USDT-M)**. This bot allows users to place MARKET and LIMIT orders with robust validation and secure authentication.

---

## 🚀 Key Features

- **Order Management**: Place MARKET and LIMIT (GTC) orders seamlessly.
- **Dual Authentication**: Supports both standard **HMAC SHA256** Secret Keys and modern **Ed25519** Private Keys.
- **Input Validation**: Comprehensive checks for symbols, sides (BUY/SELL), quantities, and price precision.
- **Structured Logging**: Automatic logging of all order requests and responses in separate log files for auditing.
- **Clean CLI**: User-friendly command-line arguments using `argparse`.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **APIs**: Binance Futures API (Testnet)
- **Libraries**: `requests`, `cryptography`, `python-dotenv`, `python-binance`

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/binance-futures-trading-bot.git
cd binance-futures-trading-bot/trading_bot
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Credentials
Create a `.env` file in the `trading_bot` directory:
```env
BINANCE_TESTNET_API_KEY=your_api_key
BINANCE_TESTNET_API_SECRET=your_secret_or_private_key
```

---

## 🖥️ Usage

Run the bot from the `trading_bot` directory.

### Place a MARKET Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

### Place a LIMIT Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 60000
```

---

## 📊 Verification & Logs

All trades are logged in the `logs/` directory:
- `logs/market_order.log`: Details of all Market order executions.
- `logs/limit_order.log`: Details of all Limit order executions.

---

## 🔒 Security Note
This bot is designed for the **Testnet** environment. Never use Mainnet API keys in a `.env` file that could be committed to version control. The `.env` file is included in `.gitignore` by default.

---

**Developed for Assignment Submission - [Your Name]**
