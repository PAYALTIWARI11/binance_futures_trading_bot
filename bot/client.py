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

BASE_URL = "https://testnet.binancefuture.com"

class BinanceClientWrapper:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_TESTNET_API_KEY')
        self.api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials missing. Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET.")

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
            
        # Add timestamp
        params['timestamp'] = int(time.time() * 1000)
        
        # Prepare payload for signing
        # Sort params by key to be deterministic
        sorted_params = sorted(params.items(), key=lambda item: item[0])
        query_string = urlencode(sorted_params)
        
        # Sign
        signature = self._get_signature(query_string)
        
        # Append signature to query_string
        full_query_string = f"{query_string}&signature={signature}"

        headers = {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        url = f"{BASE_URL}{endpoint}?{full_query_string}"
        
        print(f"DEBUG: Sending {method} to {url[:60]}...")
        print(f"DEBUG: API Key Len: {len(self.api_key)}")
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                # Send parameters in the URL (query string) for consistency
                response = requests.post(url, headers=headers) 
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            # Handle Errors logic...
            if response.status_code >= 400:
                print(f"DEBUG: Response: {response.text}")
                raise Exception(f"Binance API Error ({response.status_code}): {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise Exception(f"Request failed: {e}")
