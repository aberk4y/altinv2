#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Harem Altın Application
Tests all backend endpoints including RapidAPI integration and portfolio management
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Backend URL from frontend .env
BASE_URL = "https://harem-altin-clone.preview.emergentagent.com/api"

class HaremAltinAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.created_portfolio_items = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
        
    def test_root_endpoint(self) -> bool:
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Harem Altın API":
                    self.log_test("Root Endpoint", True, f"Response: {data}")
                    return True
                else:
                    self.log_test("Root Endpoint", False, f"Unexpected message: {data}")
                    return False
            else:
                self.log_test("Root Endpoint", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_prices_all(self) -> bool:
        """Test GET /api/prices with type='all' (default)"""
        try:
            response = self.session.get(f"{self.base_url}/prices")
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                if "lastUpdate" not in data:
                    self.log_test("Prices API (all)", False, "Missing 'lastUpdate' field")
                    return False
                
                if "gold" not in data or "currency" not in data:
                    self.log_test("Prices API (all)", False, "Missing 'gold' or 'currency' data")
                    return False
                
                # Validate gold data structure
                if not isinstance(data["gold"], list) or len(data["gold"]) == 0:
                    self.log_test("Prices API (all)", False, "Gold data is not a valid list or is empty")
                    return False
                
                # Check gold item structure
                gold_item = data["gold"][0]
                required_gold_fields = ['id', 'name', 'nameEn', 'buy', 'sell', 'change', 'unit']
                for field in required_gold_fields:
                    if field not in gold_item:
                        self.log_test("Prices API (all)", False, f"Missing field '{field}' in gold data")
                        return False
                
                # Validate currency data structure
                if not isinstance(data["currency"], list) or len(data["currency"]) == 0:
                    self.log_test("Prices API (all)", False, "Currency data is not a valid list or is empty")
                    return False
                
                # Check currency item structure
                currency_item = data["currency"][0]
                required_currency_fields = ['id', 'name', 'nameEn', 'buy', 'sell', 'change', 'symbol', 'unit']
                for field in required_currency_fields:
                    if field not in currency_item:
                        self.log_test("Prices API (all)", False, f"Missing field '{field}' in currency data")
                        return False
                
                self.log_test("Prices API (all)", True, f"Gold items: {len(data['gold'])}, Currency items: {len(data['currency'])}")
                return True
            else:
                self.log_test("Prices API (all)", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Prices API (all)", False, f"Exception: {str(e)}")
            return False
    
    def test_prices_gold_only(self) -> bool:
        """Test GET /api/prices with type='gold'"""
        try:
            response = self.session.get(f"{self.base_url}/prices?type=gold")
            if response.status_code == 200:
                data = response.json()
                
                if "lastUpdate" not in data:
                    self.log_test("Prices API (gold only)", False, "Missing 'lastUpdate' field")
                    return False
                
                if "gold" not in data:
                    self.log_test("Prices API (gold only)", False, "Missing 'gold' data")
                    return False
                
                if "currency" in data:
                    self.log_test("Prices API (gold only)", False, "Currency data should not be present when type='gold'")
                    return False
                
                if not isinstance(data["gold"], list) or len(data["gold"]) == 0:
                    self.log_test("Prices API (gold only)", False, "Gold data is not a valid list or is empty")
                    return False
                
                self.log_test("Prices API (gold only)", True, f"Gold items: {len(data['gold'])}")
                return True
            else:
                self.log_test("Prices API (gold only)", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Prices API (gold only)", False, f"Exception: {str(e)}")
            return False
    
    def test_prices_currency_only(self) -> bool:
        """Test GET /api/prices with type='currency'"""
        try:
            response = self.session.get(f"{self.base_url}/prices?type=currency")
            if response.status_code == 200:
                data = response.json()
                
                if "lastUpdate" not in data:
                    self.log_test("Prices API (currency only)", False, "Missing 'lastUpdate' field")
                    return False
                
                if "currency" not in data:
                    self.log_test("Prices API (currency only)", False, "Missing 'currency' data")
                    return False
                
                if "gold" in data:
                    self.log_test("Prices API (currency only)", False, "Gold data should not be present when type='currency'")
                    return False
                
                if not isinstance(data["currency"], list) or len(data["currency"]) == 0:
                    self.log_test("Prices API (currency only)", False, "Currency data is not a valid list or is empty")
                    return False
                
                self.log_test("Prices API (currency only)", True, f"Currency items: {len(data['currency'])}")
                return True
            else:
                self.log_test("Prices API (currency only)", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Prices API (currency only)", False, f"Exception: {str(e)}")
            return False
    
    def test_create_portfolio_gold(self) -> Optional[str]:
        """Test POST /api/portfolio - Create gold portfolio item"""
        try:
            portfolio_data = {
                "type": "gold",
                "name": "Gram Altın",
                "nameEn": "Gram Gold",
                "quantity": 10.5,
                "buyPrice": 5800.0
            }
            
            response = self.session.post(f"{self.base_url}/portfolio", json=portfolio_data)
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ['id', 'userId', 'type', 'name', 'nameEn', 'quantity', 'buyPrice', 'createdAt', 'updatedAt']
                for field in required_fields:
                    if field not in data:
                        self.log_test("Create Portfolio (Gold)", False, f"Missing field '{field}' in response")
                        return None
                
                # Validate data values
                if data['type'] != 'gold':
                    self.log_test("Create Portfolio (Gold)", False, f"Type mismatch: expected 'gold', got '{data['type']}'")
                    return None
                
                if data['quantity'] != 10.5:
                    self.log_test("Create Portfolio (Gold)", False, f"Quantity mismatch: expected 10.5, got {data['quantity']}")
                    return None
                
                if data['buyPrice'] != 5800.0:
                    self.log_test("Create Portfolio (Gold)", False, f"Buy price mismatch: expected 5800.0, got {data['buyPrice']}")
                    return None
                
                item_id = data['id']
                self.created_portfolio_items.append(item_id)
                self.log_test("Create Portfolio (Gold)", True, f"Created item with ID: {item_id}")
                return item_id
            else:
                self.log_test("Create Portfolio (Gold)", False, f"Status: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            self.log_test("Create Portfolio (Gold)", False, f"Exception: {str(e)}")
            return None
    
    def test_create_portfolio_currency(self) -> Optional[str]:
        """Test POST /api/portfolio - Create currency portfolio item"""
        try:
            portfolio_data = {
                "type": "currency",
                "name": "USD",
                "nameEn": "US Dollar",
                "quantity": 1000.0,
                "buyPrice": 34.15
            }
            
            response = self.session.post(f"{self.base_url}/portfolio", json=portfolio_data)
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ['id', 'userId', 'type', 'name', 'nameEn', 'quantity', 'buyPrice', 'createdAt', 'updatedAt']
                for field in required_fields:
                    if field not in data:
                        self.log_test("Create Portfolio (Currency)", False, f"Missing field '{field}' in response")
                        return None
                
                # Validate data values
                if data['type'] != 'currency':
                    self.log_test("Create Portfolio (Currency)", False, f"Type mismatch: expected 'currency', got '{data['type']}'")
                    return None
                
                if data['quantity'] != 1000.0:
                    self.log_test("Create Portfolio (Currency)", False, f"Quantity mismatch: expected 1000.0, got {data['quantity']}")
                    return None
                
                if data['buyPrice'] != 34.15:
                    self.log_test("Create Portfolio (Currency)", False, f"Buy price mismatch: expected 34.15, got {data['buyPrice']}")
                    return None
                
                item_id = data['id']
                self.created_portfolio_items.append(item_id)
                self.log_test("Create Portfolio (Currency)", True, f"Created item with ID: {item_id}")
                return item_id
            else:
                self.log_test("Create Portfolio (Currency)", False, f"Status: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            self.log_test("Create Portfolio (Currency)", False, f"Exception: {str(e)}")
            return None
    
    def test_get_portfolio(self) -> bool:
        """Test GET /api/portfolio - Fetch all portfolio items"""
        try:
            response = self.session.get(f"{self.base_url}/portfolio")
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Get Portfolio", False, "Response is not a list")
                    return False
                
                # If we created items, they should be in the response
                if len(self.created_portfolio_items) > 0:
                    created_ids = set(self.created_portfolio_items)
                    response_ids = set(item['id'] for item in data if 'id' in item)
                    
                    if not created_ids.issubset(response_ids):
                        missing_ids = created_ids - response_ids
                        self.log_test("Get Portfolio", False, f"Missing created items: {missing_ids}")
                        return False
                
                self.log_test("Get Portfolio", True, f"Retrieved {len(data)} portfolio items")
                return True
            else:
                self.log_test("Get Portfolio", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Get Portfolio", False, f"Exception: {str(e)}")
            return False
    
    def test_update_portfolio(self, item_id: str) -> bool:
        """Test PUT /api/portfolio/{id} - Update portfolio item"""
        try:
            update_data = {
                "quantity": 15.0,
                "buyPrice": 5850.0
            }
            
            response = self.session.put(f"{self.base_url}/portfolio/{item_id}", json=update_data)
            if response.status_code == 200:
                data = response.json()
                
                # Validate updated values
                if data.get('quantity') != 15.0:
                    self.log_test("Update Portfolio", False, f"Quantity not updated: expected 15.0, got {data.get('quantity')}")
                    return False
                
                if data.get('buyPrice') != 5850.0:
                    self.log_test("Update Portfolio", False, f"Buy price not updated: expected 5850.0, got {data.get('buyPrice')}")
                    return False
                
                # Check that updatedAt was modified
                if 'updatedAt' not in data:
                    self.log_test("Update Portfolio", False, "Missing 'updatedAt' field")
                    return False
                
                self.log_test("Update Portfolio", True, f"Updated item {item_id}")
                return True
            elif response.status_code == 404:
                self.log_test("Update Portfolio", False, f"Item not found: {item_id}")
                return False
            else:
                self.log_test("Update Portfolio", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Update Portfolio", False, f"Exception: {str(e)}")
            return False
    
    def test_delete_portfolio(self, item_id: str) -> bool:
        """Test DELETE /api/portfolio/{id} - Delete portfolio item"""
        try:
            response = self.session.delete(f"{self.base_url}/portfolio/{item_id}")
            if response.status_code == 200:
                data = response.json()
                
                if data.get('message') != "Portfolio item deleted successfully":
                    self.log_test("Delete Portfolio", False, f"Unexpected message: {data}")
                    return False
                
                # Verify item is actually deleted by trying to fetch it
                get_response = self.session.get(f"{self.base_url}/portfolio")
                if get_response.status_code == 200:
                    portfolio_items = get_response.json()
                    item_ids = [item['id'] for item in portfolio_items if 'id' in item]
                    
                    if item_id in item_ids:
                        self.log_test("Delete Portfolio", False, f"Item {item_id} still exists after deletion")
                        return False
                
                self.log_test("Delete Portfolio", True, f"Deleted item {item_id}")
                return True
            elif response.status_code == 404:
                self.log_test("Delete Portfolio", False, f"Item not found: {item_id}")
                return False
            else:
                self.log_test("Delete Portfolio", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Delete Portfolio", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_portfolio_creation(self) -> bool:
        """Test portfolio creation with invalid data"""
        try:
            # Test with invalid type
            invalid_data = {
                "type": "invalid_type",
                "name": "Test",
                "nameEn": "Test",
                "quantity": 10.0,
                "buyPrice": 100.0
            }
            
            response = self.session.post(f"{self.base_url}/portfolio", json=invalid_data)
            if response.status_code == 422:  # Validation error expected
                self.log_test("Invalid Portfolio Creation", True, "Correctly rejected invalid type")
                return True
            else:
                self.log_test("Invalid Portfolio Creation", False, f"Expected 422, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Portfolio Creation", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("=" * 60)
        print("HAREM ALTIN BACKEND API TESTS")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print()
        
        test_results = {}
        
        # Test root endpoint
        test_results['root'] = self.test_root_endpoint()
        
        # Test prices API
        test_results['prices_all'] = self.test_prices_all()
        test_results['prices_gold'] = self.test_prices_gold_only()
        test_results['prices_currency'] = self.test_prices_currency_only()
        
        # Test portfolio management
        gold_item_id = self.test_create_portfolio_gold()
        test_results['create_gold'] = gold_item_id is not None
        
        currency_item_id = self.test_create_portfolio_currency()
        test_results['create_currency'] = currency_item_id is not None
        
        test_results['get_portfolio'] = self.test_get_portfolio()
        
        # Test update and delete if we have items
        if gold_item_id:
            test_results['update_portfolio'] = self.test_update_portfolio(gold_item_id)
            test_results['delete_portfolio'] = self.test_delete_portfolio(gold_item_id)
        else:
            test_results['update_portfolio'] = False
            test_results['delete_portfolio'] = False
        
        # Clean up remaining items
        if currency_item_id:
            self.test_delete_portfolio(currency_item_id)
        
        # Test validation
        test_results['invalid_creation'] = self.test_invalid_portfolio_creation()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in test_results.values() if result)
        total = len(test_results)
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"OVERALL RESULT: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED!")
            return False

def main():
    """Main test execution"""
    tester = HaremAltinAPITester()
    success = tester.run_all_tests()
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()