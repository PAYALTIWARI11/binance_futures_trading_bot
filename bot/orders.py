from bot.client import BinanceClientWrapper
from bot.logging_config import get_logger

class OrderManager:
    def __init__(self):
        self.wrapper = BinanceClientWrapper()

    def place_market_order(self, symbol, side, quantity):
        logger = get_logger('MARKET')
        logger.info(f"Attempting MARKET order: Symbol={symbol}, Side={side}, Qty={quantity}")
        
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
            }
            
            # Use direct endpoint for Futures Order
            response = self.wrapper.send_request('POST', '/fapi/v1/order', params)
            
            logger.info(f"MARKET order success: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error (MARKET): {e}")
            raise e

    def place_limit_order(self, symbol, side, quantity, price):
        logger = get_logger('LIMIT')
        logger.info(f"Attempting LIMIT order: Symbol={symbol}, Side={side}, Qty={quantity}, Price={price}")
        
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'timeInForce': 'GTC',
                'quantity': quantity,
                'price': price
            }
            
            response = self.wrapper.send_request('POST', '/fapi/v1/order', params)
            
            logger.info(f"LIMIT order success: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error (LIMIT): {e}")
            raise e
