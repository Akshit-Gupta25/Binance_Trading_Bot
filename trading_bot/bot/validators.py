from typing import Optional


def validate_symbol(symbol: str) -> str:
    """Validate and normalize the trading symbol."""
    s = symbol.strip().upper()
    if not s or not s.isalnum():
        raise ValueError(f"Invalid symbol: '{symbol}'. Symbol must be alphanumeric (e.g., BTCUSDT).")
    return s


def validate_side(side: str) -> str:
    """Validate and normalize the trade side."""
    s = side.strip().upper()
    if s not in {"BUY", "SELL"}:
        raise ValueError(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")
    return s


def validate_order_type(order_type: str) -> str:
    """Validate and normalize the order type."""
    t = order_type.strip().upper()
    if t not in {"MARKET", "LIMIT", "STOP_LIMIT"}:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be 'MARKET', 'LIMIT', or 'STOP_LIMIT'.")
    return t


def validate_quantity(quantity: str) -> float:
    """Validate that quantity is a positive number."""
    try:
        q = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid quantity: '{quantity}'. Must be a numeric value.")
    if q <= 0:
        raise ValueError("Quantity must be a positive number.")
    return q


def validate_price(price: Optional[str]) -> Optional[float]:
    """Validate that price is a positive number if provided."""
    if price is None:
        return None
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid price: '{price}'. Must be a numeric value.")
    if p <= 0:
        raise ValueError("Price must be a positive number.")
    return p


def validate_stop_price(stop_price: Optional[str]) -> Optional[float]:
    """Validate that stop price is a positive number if provided."""
    if stop_price is None:
        return None
    try:
        sp = float(stop_price)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid stop price: '{stop_price}'. Must be a numeric value.")
    if sp <= 0:
        raise ValueError("Stop price must be a positive number.")
    return sp

