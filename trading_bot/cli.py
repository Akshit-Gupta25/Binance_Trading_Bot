import os
import sys
import argparse
import textwrap
from typing import Optional, List
from bot.client import BinanceClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.orders import place_order
from bot.logging_config import get_logger


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments with professional help messages."""
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Simplified Binance Futures Trading Bot (USDT-M Testnet)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python -m cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
              python -m cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 80000
              python -m cli --symbol BTCUSDT --side SELL --type STOP_LIMIT --quantity 0.002 --price 79000 --stop-price 79500
        """)
    )
    
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity (notional must be > 100 USDT)")
    parser.add_argument("--price", required=False, help="Order price (required for LIMIT/STOP_LIMIT)")
    parser.add_argument("--stop-price", required=False, help="Stop price (required for STOP_LIMIT)")
    parser.add_argument(
        "--base-url", 
        required=False, 
        default="https://testnet.binancefuture.com",
        help="API base URL (default: Binance Futures Testnet)"
    )
    
    return parser.parse_args(argv)


def main() -> int:
    """Main entry point for the CLI."""
    logger = get_logger("trading_bot.cli")
    args = parse_args()
    
    # 1. Validate Input
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)
        stop_price = validate_stop_price(args.stop_price)
    except ValueError as e:
        print(f"\033[91mInput Error:\033[0m {e}")
        logger.error(f"Input validation failed: {e}")
        return 2

    # 2. Check Credentials
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        print("\033[91mError:\033[0m Missing BINANCE_API_KEY or BINANCE_API_SECRET environment variables.")
        logger.error("Missing API credentials in environment.")
        return 2

    # 3. Initialize Client and Place Order
    client = BinanceClient(api_key=api_key, api_secret=api_secret, base_url=args.base_url)
    
    print("\n" + "="*40)
    print("      BINANCE FUTURES ORDER REQUEST")
    print("="*40)
    print(f" Symbol:      {symbol}")
    print(f" Side:        {side}")
    print(f" Type:        {order_type}")
    print(f" Quantity:    {quantity}")
    if price:      print(f" Price:       {price}")
    if stop_price: print(f" Stop Price:  {stop_price}")
    print("-" * 40)

    try:
        res = place_order(client, symbol, side, order_type, quantity, price, stop_price)
    except Exception as e:
        print(f"\033[91mOrder Failed:\033[0m {e}")
        logger.error(f"Order placement failed: {e}")
        return 1

    # 4. Print Summary
    order_id = res.get("orderId")
    status = res.get("status")
    executed_qty = res.get("executedQty") or res.get("cumQty") or "0"
    avg_price = res.get("avgPrice") or res.get("price") or "0"

    print("\033[92mOrder Placed Successfully!\033[0m")
    print("-" * 40)
    print(f" Order ID:    {order_id}")
    print(f" Status:      {status}")
    print(f" Executed:    {executed_qty}")
    print(f" Avg Price:   {avg_price}")
    print("="*40 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

