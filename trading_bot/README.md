# Binance Futures Trading Bot (USDT-M)

A professional, modular Python application to place orders on the Binance Futures Testnet (USDT-M). This bot supports Market, Limit, and Stop-Limit orders with robust validation, detailed logging, and a clean CLI interface.

## 🚀 Features
- **Order Types**: Support for `MARKET`, `LIMIT`, and `STOP_LIMIT` orders.
- **Robust Client**: Uses `binance-connector-python` with a custom `httpx` fallback for maximum reliability.
- **Input Validation**: Strict validation of symbols, quantities, and prices before API calls.
- **Professional Logging**: Structured logging of all requests, responses, and errors to `logs/trading_bot.log`.
- **User-Friendly CLI**: Colorized output and detailed order summaries.

## 🛠️ Project Structure
```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance API wrapper (official & custom)
│   ├── orders.py         # Order construction logic
│   ├── validators.py     # Parameter validation
│   └── logging_config.py # Centralized logging setup
├── logs/
│   └── trading_bot.log   # Application logs (created at runtime)
├── cli.py                # CLI entry point
├── requirements.txt      # Dependency list
└── README.md             # Documentation
```

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher.
- A Binance Futures Testnet account. [Register here](https://testnet.binancefuture.com).

### 2. Environment Setup
Clone the repository and create a virtual environment:
```bash
# Create venv
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. API Credentials
Set your API credentials as environment variables:
```powershell
$env:BINANCE_API_KEY="8l9CSty6zThsu0KpyvVuFJIG78DcIO2U3Z44oduJjxqYKIrUhmwoaqUyHA3bd3eD"
$env:BINANCE_API_SECRET="dhcE911CZs8UYdJ6FcR8uKdaNQSE0BAdTyOt19I0Kb2hadrVJnoMXadBIOt54W0V"
```

## 📈 Usage Examples

The bot defaults to the **Binance Futures Testnet**. You can override this with `--base-url`.

### Market Order
```bash
python -m cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

### Limit Order
```bash
python -m cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 80000
```

### Stop-Limit Order (Bonus)
```bash
python -m cli --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.002 --price 79000 --stop-price 79500
```

## 📝 Assumptions & Notes
- **Notional Value**: Binance enforces a minimum notional value (Price × Quantity) of **100 USDT** for BTCUSDT on testnet. Ensure your quantity is large enough to avoid `-4164` errors.
- **Time in Force**: Defaults to `GTC` (Good 'Til Canceled) for all limit-based orders.
- **Precision**: Quantity and price are normalized to strings to prevent floating-point precision issues during signing.

## 📄 Evaluation Deliverables
The following files are required for submission:
1. **Source Code**: All files in the `trading_bot/` directory.
2. **Requirements**: `requirements.txt` with locked versions.
3. **Logs**: A copy of `logs/trading_bot.log` containing at least one successful Market and one successful Limit order.
