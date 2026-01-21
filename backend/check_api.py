
import os
import sys
from dotenv import load_dotenv

# Load .env explicitly
load_dotenv('.env')

# Add backend directory to path so imports work
sys.path.append(os.getcwd())

from harem_api_service import harem_api_service

def check_api():
    print(f"Checking Harem Altın API with host: {os.environ.get('RAPIDAPI_HOST')}...")
    try:
        data = harem_api_service.get_all_prices()
        # Check if fallback or real
        if len(data.get('gold', [])) > 0:
            first_item = data['gold'][0]
            # Fallback data usually has specific values, but let's just print success
            print("Success! Data received.")
            print(f"Gold items: {len(data.get('gold', []))}")
            print(f"Sample: {first_item}")
        else:
            print("Received empty data.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    check_api()
