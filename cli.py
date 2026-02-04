import argparse
import sys
import json
from bot.validators import (
    validate_symbol, 
    validate_side, 
    validate_order_type, 
    validate_quantity, 
    validate_price
)
from bot.orders import OrderManager

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot (Testnet)")
    
    parser.add_argument('--symbol', type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument('--side', type=str, required=True, choices=['BUY', 'SELL'], help="Order side (BUY or SELL)")
    parser.add_argument('--type', type=str, required=True, choices=['MARKET', 'LIMIT'], dest='order_type', help="Order type (MARKET or LIMIT)")
    parser.add_argument('--qty', type=float, required=True, help="Quantity to trade")
    parser.add_argument('--price', type=float, help="Price (Required for LIMIT orders)")

    try:
        args = parser.parse_args()
        
        # --- Validation ---
        print("Validating inputs...", file=sys.stderr)
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        qty = validate_quantity(args.qty)
        price = validate_price(args.price, order_type)
        
        # --- Order Execution ---
        print(f"Initializing Order Manager...", file=sys.stderr)
        manager = OrderManager()
        
        print("\n" + "="*40)
        print(f"ORDER REQUEST SUMMARY")
        print("="*40)
        print(f"Symbol    : {symbol}")
        print(f"Side      : {side}")
        print(f"Type      : {order_type}")
        print(f"Quantity  : {qty}")
        if order_type == 'LIMIT':
            print(f"Price     : {price}")
        print("="*40 + "\n")

        print("Sending order to Binance Futures Testnet...", file=sys.stderr)
        
        if order_type == 'MARKET':
            response = manager.place_market_order(symbol, side, qty)
        else:
            response = manager.place_limit_order(symbol, side, qty, price)
            
        # --- Output Response ---
        print("SUCCESS! Order placed.")
        print("-" * 30)
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty', '0')}") # Often 0 for Limit initially
        print(f"Avg Price    : {response.get('avgPrice', '0')}")
        print("-" * 30)

    except ValueError as ve:
        print(f"\n[VALIDATION ERROR]: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[EXECUTION FAILED]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
