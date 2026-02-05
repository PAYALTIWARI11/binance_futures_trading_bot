import os
import time
from bot.client import BinanceClientWrapper

def test_connectivity():
    client = BinanceClientWrapper()
    print("Testing connectivity to Binance Futures Testnet...")
    try:
        # Test basic connectivity with an unsigned request first
        response = client.send_request('GET', '/fapi/v1/ticker/price', {'symbol': 'BTCUSDT'})
        print(f"Successfully fetched BTC price: {response.get('price')}")
        return True
    except Exception as e:
        print(f"Connectivity test failed: {e}")
        return False


if __name__ == "__main__":
    test_connectivity()
