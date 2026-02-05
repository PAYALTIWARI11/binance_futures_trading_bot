def validate_symbol(symbol):
    """
    Validates the trading symbol.
    Must be alphanumeric and uppercase.
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    if not symbol.isalnum():
        raise ValueError(f"Symbol '{symbol}' contains invalid characters. Alphanumeric only.")
    if not symbol.isupper():
        raise ValueError(f"Symbol '{symbol}' must be uppercase.")
    return symbol

def validate_side(side):
    """
    Validates side: BUY or SELL.
    """
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid side '{side}'. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type):
    """
    Validates order type: MARKET, LIMIT, or TRAILING_STOP_MARKET.
    """
    allowed = ['MARKET', 'LIMIT', 'TRAILING_STOP_MARKET']
    if order_type not in allowed:
        raise ValueError(f"Invalid order_type '{order_type}'. Must be one of {allowed}.")
    return order_type




def validate_quantity(qty):
    """
    Validates quantity: Must be a positive float.
    """
    if qty is None:
        raise ValueError("Quantity is required.")
    try:
        qty = float(qty)
    except ValueError:
        raise ValueError(f"Quantity '{qty}' is not a valid number.")
    
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {qty}")
    return qty

def validate_price(price, order_type):
    """
    Validates price: Required and > 0 if order_type is LIMIT.
    """
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            price = float(price)
        except ValueError:
            raise ValueError(f"Price '{price}' is not a valid number.")
        
        if price <= 0:
            raise ValueError(f"Price must be greater than 0. Got: {price}")
    return price

def validate_callback_rate(rate, order_type):
    """
    Validates callback rate: Required and 0.1 to 5.0 for TRAILING_STOP_MARKET.
    """
    if order_type == 'TRAILING_STOP_MARKET':
        if rate is None:
            raise ValueError("Callback Rate is required for TRAILING_STOP_MARKET.")
        try:
            rate = float(rate)
        except ValueError:
            raise ValueError(f"Callback Rate '{rate}' is not a valid number.")
        
        if not (0.1 <= rate <= 5.0):
            raise ValueError(f"Callback Rate must be between 0.1 and 5.0. Got: {rate}")
    return rate


