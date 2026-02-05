import requests

def test_ping():
    base_url = "https://testnet.binancefuture.com"
    endpoint = "/fapi/v1/ping"
    try:
        response = requests.get(f"{base_url}{endpoint}")
        print(f"Ping Status Code: {response.status_code}")
        print(f"Ping Response: {response.json()}")
    except Exception as e:
        print(f"Ping failed: {e}")

if __name__ == "__main__":
    test_ping()
