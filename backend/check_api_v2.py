
import os
import sys
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env')

KEY = os.environ.get('RAPIDAPI_KEY')
HOST = os.environ.get('RAPIDAPI_HOST')

def check_new_endpoint():
    url = f"https://{HOST}/economy/live-exchange-rates/list"
    print(f"Requesting {url}...")
    
    headers = {
        "x-rapidapi-key": KEY,
        "x-rapidapi-host": HOST
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response structure keys:", data.keys())
            
            if 'data' in data and len(data['data']) > 0:
                first_item = data['data'][0]
                print("\nFirst item keys:", first_item.keys())
                print("First item content:", json.dumps(first_item, indent=2))
                
                # Check for price fields
                if 'buy' in first_item or 'sell' in first_item or 'price' in first_item:
                    print("\nSUCCESS: Price data found!")
                else:
                    print("\nWARNING: No price fields found in this endpoint. It might be just a list of codes.")
            else:
                print("Data list is empty.")
        else:
            print("Error response:", response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_new_endpoint()
