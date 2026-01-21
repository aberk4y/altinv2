
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env')

KEY = os.environ.get('RAPIDAPI_KEY')
HOST = os.environ.get('RAPIDAPI_HOST')

def inspect_item():
    url = f"https://{HOST}/economy/live-exchange-rates"
    headers = {
        "x-rapidapi-key": KEY,
        "x-rapidapi-host": HOST
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                print(json.dumps(data['data'][0], indent=2))
                # Also print one gold item if possible
                for item in data['data']:
                    if 'ALTIN' in item.get('code', '').upper() or 'ALTIN' in item.get('currencyCode', '').upper():
                        print("\nGold Item:")
                        print(json.dumps(item, indent=2))
                        break
            else:
                print("No data found")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_item()
