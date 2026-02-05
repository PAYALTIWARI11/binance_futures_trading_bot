from bot.client import BinanceClientWrapper
from bot.logging_config import get_logger

class OrderManager:
    def __init__(self):
        self.wrapper = BinanceClientWrapper()

    def _place_order(self, params, order_type_name):
        logger = get_logger(order_type_name)
        logger.info(f"Attempting {order_type_name} order: {params}")
        
        try:
            response = self.wrapper.send_request('POST', '/fapi/v1/order', params)
            logger.info(f"{order_type_name} order success: {response}")
            return response
        except Exception as e:
            logger.error(f"Error ({order_type_name}): {e}")
            raise e

    def place_market_order(self, symbol, side, quantity):
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity,
        }
        return self._place_order(params, 'MARKET')

    def place_limit_order(self, symbol, side, quantity, price):
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': quantity,
            'price': price
        }
        return self._place_order(params, 'LIMIT')

    def place_trailing_stop_market_order(self, symbol, side, quantity, callback_rate):
        """
        Bonus: Add a third order type: Trailing Stop Market
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'TRAILING_STOP_MARKET',
            'quantity': quantity,
            'callbackRate': callback_rate, # e.g. 1.0 for 1%
            'workingType': 'MARK_PRICE'
        }
        return self._place_order(params, 'TRAILING_STOP_MARKET')





