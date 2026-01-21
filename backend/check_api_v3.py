
import os
import sys
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env')

KEY = os.environ.get('RAPIDAPI_KEY')
HOST = os.environ.get('RAPIDAPI_HOST')

def check_endpoints_v3():
    print(f"Testing paths on {HOST}...")
    headers = {
        "x-rapidapi-key": KEY,
        "x-rapidapi-host": HOST
    }
    
    # Try getting specific rate for a code from the list
    test_code = "USDTRY"
    paths_to_try = [
        f"/economy/live-exchange-rates/{test_code}",
        "/economy/live-exchange-rates",
        "/economy/live-exchange-rates/all",
        "/prices",
        "/gold/prices"
    ]
    
    for path in paths_to_try:
        url = f"https://{HOST}{path}"
        try:
            print(f"Trying {path}...", end=" ")
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS!")
                print("First 200 chars:", response.text[:200])
                if len(response.text) > 200:
                     print("... content truncated")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_endpoints_v3()
