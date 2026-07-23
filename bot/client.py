import os
import logging
from logging.handlers import RotatingFileHandler
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
#SETUP
logger = logging.getLogger("TradingBot")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler = RotatingFileHandler("trading_bot.log", maxBytes=5*1024*1024, backupCount=2)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

class BinanceBot:
    def __init__(self):
         # initialized
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.error("API keys missing.")
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in the environment.")

        # Initialize the client
        self.client = Client(api_key, api_secret, testnet=True)
        
        # Explicitly use the testnet base URL to satisfy project requirements
        BASE_URL = "https://testnet.binancefuture.com"
        self.client.FUTURES_URL = BASE_URL
        
        try:
            self.client.futures_time()
            logger.info("Successfully conected to Binance Futures Testnet.")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        side = side.upper()
        order_type = order_type.upper()

        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        if order_type not in ["MARKET", "LIMIT"]:
            raise ValueError("Order type must be MARKET or LIMIT")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        order_params = {
            'symbol': symbol.upper(),
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        if order_type == 'LIMIT':
            if price is None or price <= 0:
                raise ValueError("A valid price must be provided for LIMIT orders.")
            order_params['price'] = price
            order_params['timeInForce'] = 'GTC'

        logger.info(f"Placing order: {order_params}")

        try:
            response = self.client.futures_create_order(**order_params)
            logger.info(f"Order sucessful. Response: {response}")
            return response
        except BinanceAPIException as e:
            logger.error(f"API Error: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unepected error: {e}")
            raise
