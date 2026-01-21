
import requests
import json

def check_alternative_api():
    url = "https://harem-altin-live-gold-price-data.p.rapidapi.com/harem_altin/prices/23b4c2fb31a242d1eebc0df9b9b65e5e"
    
    headers = {
        "x-rapidapi-key": "1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4",
        "x-rapidapi-host": "harem-altin-live-gold-price-data.p.rapidapi.com"
    }
    
    print(f"Testing URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nResponse Body (First 500 chars):")
            print(json.dumps(data, indent=2)[:500])
            
            if 'data' in data or 'success' in data:
                print("\nSUCCESS: Looks like valid JSON data.")
            else:
                print("\nWARNING: JSON received but structure is unknown.")
        else:
            print(f"\nError: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    check_alternative_api()
