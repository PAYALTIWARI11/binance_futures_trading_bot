import argparse
import sys
import json
from bot.validators import (
    validate_symbol, 
    validate_side, 
    validate_order_type, 
    validate_quantity, 
    validate_price,
    validate_callback_rate
)

from bot.orders import OrderManager

def get_interactive_input():
    """
    Bonus: Add an enhanced CLI UX (menus, prompts, validation messages)
    """
    print("\n--- Binance Futures Bot Interactive Mode ---")
    symbol = input("Enter symbol (e.g. BTCUSDT): ").upper().strip()
    side = input("Enter side (BUY/SELL): ").upper().strip()
    order_type = input("Enter order type (MARKET/LIMIT/TRAILING_STOP_MARKET): ").upper().strip()

    qty = input("Enter quantity: ").strip()
    
    price = None
    if order_type == 'LIMIT':
        price = input("Enter limit price: ").strip()
        
    callback_rate = None
    if order_type == 'TRAILING_STOP_MARKET':
        callback_rate = input("Enter callback rate (0.1 to 5.0): ").strip()


        
    return symbol, side, order_type, qty, price, callback_rate


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot (Testnet)")
    
    parser.add_argument('--symbol', type=str, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument('--side', type=str, choices=['BUY', 'SELL'], help="Order side (BUY or SELL)")
    parser.add_argument('--type', type=str, choices=['MARKET', 'LIMIT', 'TRAILING_STOP_MARKET'], dest='order_type', help="Order type")
    parser.add_argument('--qty', type=float, help="Quantity to trade")
    parser.add_argument('--price', type=float, help="Price (Required for LIMIT orders)")
    parser.add_argument('--callback_rate', type=float, help="Callback Rate (Required for TRAILING_STOP_MARKET)")

    try:
        args = parser.parse_args()
        
        # Check if we should enter interactive mode (if any required arg is missing)
        if not all([args.symbol, args.side, args.order_type, args.qty]):
            symbol, side, order_type, qty, price, callback_rate = get_interactive_input()
        else:
            symbol = args.symbol
            side = args.side
            order_type = args.order_type
            qty = args.qty
            price = args.price
            callback_rate = args.callback_rate

        # --- Validation ---
        print("Validating inputs...", file=sys.stderr)
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        qty = validate_quantity(qty)
        price = validate_price(price, order_type)
        callback_rate = validate_callback_rate(callback_rate, order_type)
        
        # --- Order Execution ---
        manager = OrderManager()
        
        print("\n" + "="*40)
        print(f"ORDER REQUEST SUMMARY")
        print("="*40)
        print(f"Symbol        : {symbol}")
        print(f"Side          : {side}")
        print(f"Type          : {order_type}")
        print(f"Quantity      : {qty}")
        if order_type == 'LIMIT':
            print(f"Price         : {price}")
        if order_type == 'TRAILING_STOP_MARKET':
            print(f"Callback Rate : {callback_rate}%")
        print("="*40 + "\n")

        print("Sending order to Binance Futures Testnet...", file=sys.stderr)
        
        if order_type == 'MARKET':
            response = manager.place_market_order(symbol, side, qty)
        elif order_type == 'LIMIT':
            response = manager.place_limit_order(symbol, side, qty, price)
        elif order_type == 'TRAILING_STOP_MARKET':
            response = manager.place_trailing_stop_market_order(symbol, side, qty, callback_rate)

            
        # --- Output Response ---
        print("SUCCESS! Order placed.")
        print("-" * 30)
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty', '0')}")
        print(f"Avg Price    : {response.get('avgPrice', '0')}")
        print("-" * 30)

    except (ValueError, KeyboardInterrupt) as ve:
        print(f"\n[ERROR]: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[EXECUTION FAILED]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
