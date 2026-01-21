
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv('.env')

KEY = os.environ.get('RAPIDAPI_KEY')
HOST = os.environ.get('RAPIDAPI_HOST')

headers = {
    "x-rapidapi-key": KEY,
    "x-rapidapi-host": HOST
}

paths_to_try = [
    "/harem_altin/prices", # Original
    "/prices",
    "/gold",
    "/currency",
    "/",
    "/api/prices",
    "/data",
    "/list"
]

def check_endpoints():
    print(f"Testing paths on {HOST}...")
    
    for path in paths_to_try:
        url = f"https://{HOST}{path}"
        try:
            print(f"Trying {path}...", end=" ")
            response = requests.get(url, headers=headers, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS!")
                print("First 100 chars:", response.text[:100])
                return
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_endpoints()
