import os
import time
import base64
import logging
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Load environment variables
load_dotenv()

# Environment configuration
BINANCE_ENV = os.getenv('BINANCE_ENV', 'testnet').lower()

if BINANCE_ENV == 'production':
    BASE_URL = "https://fapi.binance.com"
    API_KEY_VAR = 'BINANCE_API_KEY'
    API_SECRET_VAR = 'BINANCE_API_SECRET'
else:
    BASE_URL = "https://testnet.binancefuture.com"
    API_KEY_VAR = 'BINANCE_TESTNET_API_KEY'
    API_SECRET_VAR = 'BINANCE_TESTNET_API_SECRET'

class BinanceClientWrapper:
    def __init__(self):
        self.api_key = os.getenv(API_KEY_VAR)
        self.api_secret = os.getenv(API_SECRET_VAR)
        
        if not self.api_key or not self.api_secret:
            raise ValueError(f"API credentials missing. Please set {API_KEY_VAR} and {API_SECRET_VAR} for {BINANCE_ENV} environment.")


        # Strip whitespace just in case
        self.api_key = self.api_key.strip()
        self.api_secret = self.api_secret.strip()

        # Try loading as Ed25519 (Private Key)
        self.private_key = None
        if len(self.api_secret) > 100 or "-----BEGIN" in self.api_secret:
            try:
                if "-----BEGIN PRIVATE KEY-----" not in self.api_secret:
                    pem_key = f"-----BEGIN PRIVATE KEY-----\n{self.api_secret}\n-----END PRIVATE KEY-----"
                else:
                    pem_key = self.api_secret
                
                self.private_key = load_pem_private_key(
                    pem_key.encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )
            except Exception:
                # If it's not a valid Ed25519 key, we assume it's an HMAC secret
                self.private_key = None

    def _get_signature(self, payload):
        if self.private_key:
            # Ed25519 signing
            signature = self.private_key.sign(payload.encode('utf-8'))
            return base64.b64encode(signature).decode('utf-8')
        else:
            # HMAC SHA256 signing (Standard for system-generated keys)
            import hmac
            import hashlib
            return hmac.new(
                self.api_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

    def send_request(self, method, endpoint, params=None):
        if params is None:
            params = {}
            
        # Add mandatory timestamp and optional recvWindow
        params['timestamp'] = int(time.time() * 1000)
        if 'recvWindow' not in params:
            params['recvWindow'] = 5000
        
        # Prepare and sign the query string
        query_string = urlencode(sorted(params.items()))
        signature = self._get_signature(query_string)
        full_query_string = f"{query_string}&signature={signature}"

        headers = {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"{BASE_URL}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(f"{url}?{full_query_string}", headers=headers)
            elif method.upper() == 'POST':
                # Binance requires parameters for signed POST requests to be in the query string 
                # OR in the body. Putting them in query string is usually more reliable across endpoints.
                response = requests.post(f"{url}?{full_query_string}", headers=headers)
            elif method.upper() == 'DELETE':
                response = requests.delete(f"{url}?{full_query_string}", headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            # Log the full request and response for transparency (as per requirements)
            logging.debug(f"API Request: {method} {url} Params: {params}")
            logging.debug(f"API Response: {response.status_code} {response.text}")

            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('msg', 'Unknown Error')
                error_code = error_data.get('code', 'N/A')
                raise Exception(f"Binance API Error {error_code}: {error_msg}")
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error occurred: {e}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")

