from typing import Dict, Any, Optional
from .client import BinanceClient
from .logging_config import get_logger


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    time_in_force: str = "GTC",
) -> Dict[str, Any]:
    """
    Construct and place an order on Binance Futures.

    :param client: BinanceClient instance.
    :param symbol: Trading pair symbol (e.g., 'BTCUSDT').
    :param side: 'BUY' or 'SELL'.
    :param order_type: 'MARKET', 'LIMIT', or 'STOP_LIMIT'.
    :param quantity: Quantity to trade.
    :param price: Order price (required for LIMIT and STOP_LIMIT).
    :param stop_price: Stop price (required for STOP_LIMIT).
    :param time_in_force: TIF policy (default: 'GTC').
    :return: API response dictionary.
    :raises ValueError: If required parameters are missing for the order type.
    """
    logger = get_logger("trading_bot.orders")
    
    # Base parameters for all order types
    params: Dict[str, Any] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": str(quantity),
    }

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Limit price is required for LIMIT orders.")
        params["price"] = str(price)
        params["timeInForce"] = time_in_force
        
    elif order_type == "MARKET":
        # Market orders don't require price or TIF
        pass
        
    elif order_type == "STOP_LIMIT":
        if price is None or stop_price is None:
            raise ValueError("Both price and stop_price are required for STOP_LIMIT orders.")
        params["price"] = str(price)
        params["stopPrice"] = str(stop_price)
        params["timeInForce"] = time_in_force
        # Map STOP_LIMIT to Binance STOP order type
        params["type"] = "STOP"
        
    else:
        raise ValueError(f"Unsupported order type: {order_type}")

    logger.info(f"Constructed order request: {params}")
    
    try:
        res = client.create_order(params)
        logger.info(f"Order successfully placed: {res}")
        return res
    except Exception as e:
        logger.error(f"Failed to place order: {str(e)}")
        raise
