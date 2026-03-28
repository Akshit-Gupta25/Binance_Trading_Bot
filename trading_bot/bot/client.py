import time
import hmac
import hashlib
from typing import Any, Dict, Optional
import httpx
from .logging_config import get_logger

try:
    from binance.um_futures import UMFutures
    _HAS_CONNECTOR = True
except (ImportError, Exception):
    UMFutures = None  # type: ignore
    _HAS_CONNECTOR = False


class BinanceClient:
    """
    Client for interacting with Binance Futures API.
    Supports both official binance-connector-python and a direct REST fallback.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        """
        Initialize the client.
        
        :param api_key: Binance API Key
        :param api_secret: Binance API Secret
        :param base_url: API Base URL (default: testnet)
        """
        self.base_url = base_url.rstrip("/")
        self.logger = get_logger("trading_bot.client")

        if _HAS_CONNECTOR and UMFutures:
            self.logger.info("Using official binance-connector-python client.")
            self.um = UMFutures(api_key=api_key, api_secret=api_secret, base_url=self.base_url)
            self.http = None
            self.api_key = None
            self.api_secret = None
        else:
            self.logger.info("Official connector not found. Falling back to direct REST client.")
            self.um = None
            self.http = httpx.Client(
                timeout=httpx.Timeout(10.0, connect=10.0),
                headers={"X-MBX-APIKEY": api_key}
            )
            self.api_key = api_key
            self.api_secret = api_secret

    def _sign(self, params: Dict[str, Any]) -> str:
        """Sign parameters using HMAC SHA256."""
        query = "&".join(f"{k}={params[k]}" for k in params.keys())
        return hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()  # type: ignore[union-attr]

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, signed: bool = True) -> Dict[str, Any]:
        """Perform a REST request."""
        url = f"{self.base_url}{path}"
        params = params or {}
        
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 5000
            params["signature"] = self._sign(params)

        self.logger.info(f"Request: {method} {url} {params}")
        
        try:
            if method.upper() == "GET":
                r = self.http.get(url, params=params)  # type: ignore[union-attr]
            elif method.upper() == "POST":
                r = self.http.post(url, params=params)  # type: ignore[union-attr]
            else:
                raise RuntimeError(f"Unsupported HTTP method: {method}")
            
            r.raise_for_status()
            response_json = r.json()
            self.logger.info(f"Response ({r.status_code}): {response_json}")
            return response_json

        except httpx.HTTPStatusError as e:
            self.logger.error(f"API Error ({e.response.status_code}): {e.response.text}")
            raise RuntimeError(f"Binance API error: {e.response.text}")
        except Exception as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise RuntimeError(f"Network or system error: {str(e)}")

    def create_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order.
        
        :param params: Dictionary of order parameters.
        :return: API response.
        """
        if self.um:
            self.logger.info(f"Placing order via UMFutures: {params}")
            try:
                res = self.um.new_order(**params)
                self.logger.info(f"Order response: {res}")
                return res
            except Exception as e:
                self.logger.error(f"UMFutures order failed: {str(e)}")
                raise RuntimeError(f"Order creation failed: {str(e)}")
        
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)

    def ping(self) -> Dict[str, Any]:
        """Check server connectivity."""
        if self.um:
            return self.um.ping()
        return self._request("GET", "/fapi/v1/ping", signed=False)
