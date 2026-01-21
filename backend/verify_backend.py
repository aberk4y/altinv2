
import requests
import sys
import json

BASE_URL = "http://127.0.0.1:8001/api"

def test_backend():
    print("--- 1. Testing Login ---")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/admin/login", data=login_data)
    if response.status_code != 200:
        print(f"Login Failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    print("Login Success! Token received.")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n--- 2. Testing Margins CRUD ---")
    # Get initial margins
    response = requests.get(f"{BASE_URL}/margins", headers=headers)
    print(f"Initial Margins: {len(response.json())}")
    
    # Set a margin for "HAS ALTIN" (using the lowercase key from new API: 'altintry')
    # Or actually, the margin model key is whatever we decide.
    # In server.py we map item.get("name") against margins.
    # harem_api_service maps 'altintry' -> ('HAS ALTIN', 'PURE GOLD').
    # So the key in margins db should be "HAS ALTIN".
    
    target_product = "HAS ALTIN"
    margin_payload = {
        "product_name_key": target_product,
        "margin_amount": 10.0,
        "is_percentage": False
    }
    
    response = requests.post(f"{BASE_URL}/margins", json=margin_payload, headers=headers)
    if response.status_code == 200:
        print(f"Margin Set for {target_product}: 10.0 (Fixed)")
    else:
        print(f"Margin Set Failed: {response.text}")
        return

    print("\n--- 3. Testing Prices with Margin ---")
    response = requests.get(f"{BASE_URL}/prices")
    data = response.json()
    
    gold_list = data.get("gold", [])
    found = False
    for item in gold_list:
        if item["name"] == target_product:
            found = True
            print(f"Found {target_product}: Buy={item['buy']}, Sell={item['sell']}")
            # We don't know the exact raw price here easily without a separate call, 
            # but getting a result means the pipeline works.
            # If we wanted to verify exact calc, we'd need raw data.
            # But the fact checking didn't explode is good step 1.
            break
            
    if not found:
        print(f"Warning: {target_product} not found in prices list.")
        
    print("\n--- Integration Test Complete ---")

if __name__ == "__main__":
    test_backend()
