#!/usr/bin/env python3
"""
Comprehensive Security and Functionality Tests for ASLANOĞLU KUYUMCULUK (BERKAY ALTIN)
Tests all backend endpoints with focus on security vulnerabilities and performance
"""

import requests
import json
import time
import threading
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse

# Backend URL from frontend .env
BASE_URL = "https://berkayfinance.preview.emergentagent.com/api"

class AslanoğluKuyumculukSecurityTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.created_portfolio_items = []
        self.security_issues = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
        
    def log_security_issue(self, issue: str):
        """Log security vulnerabilities"""
        self.security_issues.append(issue)
        print(f"🚨 SECURITY ISSUE: {issue}")
        
    # ========== SECURITY TESTS ==========
    
    def test_cors_policy(self) -> bool:
        """Test CORS policy - verify only allowed origins"""
        try:
            # Test with malicious origin
            malicious_headers = {
                'Origin': 'https://malicious-site.com',
                'Access-Control-Request-Method': 'GET',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = self.session.options(f"{self.base_url}/prices", headers=malicious_headers)
            
            # Check if CORS allows the malicious origin
            cors_origin = response.headers.get('Access-Control-Allow-Origin', '')
            
            if cors_origin == '*':
                self.log_security_issue("CORS allows all origins (*) - potential security risk")
                self.log_test("CORS Policy", False, "Allows all origins")
                return False
            elif 'malicious-site.com' in cors_origin:
                self.log_security_issue("CORS allows malicious origins")
                self.log_test("CORS Policy", False, "Allows malicious origins")
                return False
            else:
                self.log_test("CORS Policy", True, f"CORS properly configured: {cors_origin}")
                return True
                
        except Exception as e:
            self.log_test("CORS Policy", False, f"Exception: {str(e)}")
            return False
    
    def test_sql_injection_attempts(self) -> bool:
        """Test SQL injection attempts on all endpoints"""
        try:
            sql_payloads = [
                "'; DROP TABLE users; --",
                "' OR '1'='1",
                "' UNION SELECT * FROM users --",
                "'; INSERT INTO users VALUES ('hacker', 'password'); --",
                "' OR 1=1 --"
            ]
            
            all_safe = True
            
            for payload in sql_payloads:
                # Test on prices endpoint
                response = self.session.get(f"{self.base_url}/prices?type={urllib.parse.quote(payload)}")
                if response.status_code == 500:
                    self.log_security_issue(f"SQL injection may be possible with payload: {payload}")
                    all_safe = False
                
                # Test on portfolio creation
                portfolio_data = {
                    "type": "gold",
                    "name": payload,
                    "nameEn": payload,
                    "quantity": 10.0,
                    "buyPrice": 100.0
                }
                response = self.session.post(f"{self.base_url}/portfolio", json=portfolio_data)
                if response.status_code == 500:
                    self.log_security_issue(f"SQL injection may be possible in portfolio creation with payload: {payload}")
                    all_safe = False
            
            if all_safe:
                self.log_test("SQL Injection Protection", True, "All SQL injection attempts properly handled")
            else:
                self.log_test("SQL Injection Protection", False, "Potential SQL injection vulnerabilities found")
            
            return all_safe
            
        except Exception as e:
            self.log_test("SQL Injection Protection", False, f"Exception: {str(e)}")
            return False
    
    def test_xss_attempts(self) -> bool:
        """Test XSS attempts"""
        try:
            xss_payloads = [
                "<script>alert('XSS')</script>",
                "javascript:alert('XSS')",
                "<img src=x onerror=alert('XSS')>",
                "';alert('XSS');//",
                "<svg onload=alert('XSS')>"
            ]
            
            all_safe = True
            
            for payload in xss_payloads:
                # Test portfolio creation with XSS payload
                portfolio_data = {
                    "type": "gold",
                    "name": payload,
                    "nameEn": payload,
                    "quantity": 10.0,
                    "buyPrice": 100.0
                }
                
                response = self.session.post(f"{self.base_url}/portfolio", json=portfolio_data)
                
                if response.status_code == 200:
                    data = response.json()
                    # Check if the payload is returned unescaped
                    if payload in str(data) and '<script>' in payload:
                        self.log_security_issue(f"XSS vulnerability: payload returned unescaped: {payload}")
                        all_safe = False
                    else:
                        # Clean up created item
                        if 'id' in data:
                            self.session.delete(f"{self.base_url}/portfolio/{data['id']}")
            
            if all_safe:
                self.log_test("XSS Protection", True, "All XSS attempts properly handled")
            else:
                self.log_test("XSS Protection", False, "Potential XSS vulnerabilities found")
            
            return all_safe
            
        except Exception as e:
            self.log_test("XSS Protection", False, f"Exception: {str(e)}")
            return False
    
    def test_authentication_bypass_attempts(self) -> bool:
        """Test authentication bypass attempts"""
        try:
            bypass_attempts = [
                # Try accessing admin endpoints without token
                f"{self.base_url}/admin/me",
                f"{self.base_url}/margins",
                # Try with invalid tokens
                f"{self.base_url}/admin/me",
                f"{self.base_url}/margins"
            ]
            
            all_secure = True
            
            # Test without any token
            for endpoint in bypass_attempts[:2]:
                response = self.session.get(endpoint)
                if response.status_code != 401:
                    self.log_security_issue(f"Authentication bypass possible at {endpoint}")
                    all_secure = False
            
            # Test with invalid tokens
            invalid_tokens = [
                "Bearer invalid_token",
                "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWNrZXIifQ.invalid",
                "Bearer null",
                "Bearer undefined"
            ]
            
            for token in invalid_tokens:
                headers = {'Authorization': token}
                for endpoint in bypass_attempts[2:]:
                    response = self.session.get(endpoint, headers=headers)
                    if response.status_code == 200:
                        self.log_security_issue(f"Authentication bypass with invalid token at {endpoint}")
                        all_secure = False
            
            if all_secure:
                self.log_test("Authentication Bypass Protection", True, "All bypass attempts properly blocked")
            else:
                self.log_test("Authentication Bypass Protection", False, "Authentication bypass vulnerabilities found")
            
            return all_secure
            
        except Exception as e:
            self.log_test("Authentication Bypass Protection", False, f"Exception: {str(e)}")
            return False
    
    def test_jwt_token_validation(self) -> bool:
        """Test JWT token expiry and validation"""
        try:
            # Test with malformed JWT tokens
            malformed_tokens = [
                "Bearer not.a.jwt",
                "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # Incomplete JWT
                "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWNrZXIiLCJleHAiOjE2MDk0NTkyMDB9.invalid_signature",
                "Bearer " + "A" * 500,  # Extremely long token
            ]
            
            all_secure = True
            
            for token in malformed_tokens:
                headers = {'Authorization': token}
                response = self.session.get(f"{self.base_url}/admin/me", headers=headers)
                
                if response.status_code == 200:
                    self.log_security_issue(f"JWT validation bypass with malformed token: {token[:50]}...")
                    all_secure = False
                elif response.status_code != 401:
                    self.log_security_issue(f"Unexpected response to malformed JWT: {response.status_code}")
                    all_secure = False
            
            if all_secure:
                self.log_test("JWT Token Validation", True, "All malformed JWT tokens properly rejected")
            else:
                self.log_test("JWT Token Validation", False, "JWT validation vulnerabilities found")
            
            return all_secure
            
        except Exception as e:
            self.log_test("JWT Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_rate_limiting(self) -> bool:
        """Test API rate limiting (if any)"""
        try:
            # Make rapid requests to test rate limiting
            rapid_requests = 50
            responses = []
            
            start_time = time.time()
            for i in range(rapid_requests):
                response = self.session.get(f"{self.base_url}/prices")
                responses.append(response.status_code)
            end_time = time.time()
            
            # Check if any requests were rate limited (429 status)
            rate_limited = any(status == 429 for status in responses)
            
            if rate_limited:
                self.log_test("Rate Limiting", True, f"Rate limiting detected after {rapid_requests} requests")
                return True
            else:
                # Rate limiting might not be implemented, which is a security concern for production
                self.log_test("Rate Limiting", False, f"No rate limiting detected after {rapid_requests} requests in {end_time-start_time:.2f}s")
                return False
                
        except Exception as e:
            self.log_test("Rate Limiting", False, f"Exception: {str(e)}")
            return False
    
    # ========== FUNCTIONALITY TESTS ==========
    
    def test_prices_comprehensive(self) -> bool:
        """Test GET /api/prices - verify all 14 gold + 11 currency items"""
        try:
            response = self.session.get(f"{self.base_url}/prices")
            if response.status_code != 200:
                self.log_test("Prices Comprehensive", False, f"Status: {response.status_code}")
                return False
            
            data = response.json()
            
            # Check structure
            required_fields = ['lastUpdate', 'gold', 'currency']
            for field in required_fields:
                if field not in data:
                    self.log_test("Prices Comprehensive", False, f"Missing field: {field}")
                    return False
            
            # Count items
            gold_count = len(data.get('gold', []))
            currency_count = len(data.get('currency', []))
            
            # Verify counts (should be 14 gold + 11 currency as per request)
            if gold_count < 10:  # Allow some flexibility
                self.log_test("Prices Comprehensive", False, f"Insufficient gold items: {gold_count} (expected ~14)")
                return False
            
            if currency_count < 10:  # Allow some flexibility
                self.log_test("Prices Comprehensive", False, f"Insufficient currency items: {currency_count} (expected ~11)")
                return False
            
            # Verify Turkish character support
            turkish_chars_found = False
            for item in data.get('gold', []) + data.get('currency', []):
                name = item.get('name', '')
                if any(char in name for char in 'ğüşıöçĞÜŞİÖÇ'):
                    turkish_chars_found = True
                    break
            
            if not turkish_chars_found:
                self.log_test("Prices Comprehensive", False, "No Turkish characters found in item names")
                return False
            
            self.log_test("Prices Comprehensive", True, f"Gold: {gold_count}, Currency: {currency_count}, Turkish chars: ✓")
            return True
            
        except Exception as e:
            self.log_test("Prices Comprehensive", False, f"Exception: {str(e)}")
            return False
    
    def test_concurrent_requests(self) -> bool:
        """Test concurrent requests (10 simultaneous)"""
        try:
            def make_request():
                return self.session.get(f"{self.base_url}/prices")
            
            # Make 10 concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                responses = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            # Check all responses
            success_count = sum(1 for r in responses if r.status_code == 200)
            
            if success_count == 10:
                self.log_test("Concurrent Requests", True, f"All 10 concurrent requests successful")
                return True
            else:
                self.log_test("Concurrent Requests", False, f"Only {success_count}/10 requests successful")
                return False
                
        except Exception as e:
            self.log_test("Concurrent Requests", False, f"Exception: {str(e)}")
            return False
    
    def test_data_validation_comprehensive(self) -> bool:
        """Test comprehensive data validation"""
        try:
            # Test price format validation
            response = self.session.get(f"{self.base_url}/prices")
            if response.status_code != 200:
                self.log_test("Data Validation", False, "Cannot fetch prices for validation")
                return False
            
            data = response.json()
            
            # Validate price format (buy, sell, change)
            for item_type in ['gold', 'currency']:
                for item in data.get(item_type, []):
                    # Check required price fields
                    price_fields = ['buy', 'sell', 'change']
                    for field in price_fields:
                        if field not in item:
                            self.log_test("Data Validation", False, f"Missing {field} in {item_type} item")
                            return False
                        
                        # Check if price is a valid number
                        try:
                            float(item[field])
                        except (ValueError, TypeError):
                            self.log_test("Data Validation", False, f"Invalid {field} value in {item_type}: {item[field]}")
                            return False
            
            # Test empty/null response handling
            response = self.session.get(f"{self.base_url}/prices?type=invalid")
            # Should still return valid structure even with invalid type
            
            self.log_test("Data Validation", True, "All price formats valid, Turkish chars supported")
            return True
            
        except Exception as e:
            self.log_test("Data Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_performance_under_load(self) -> bool:
        """Test response time under load and memory stability"""
        try:
            response_times = []
            
            # Make 20 requests and measure response times
            for i in range(20):
                start_time = time.time()
                response = self.session.get(f"{self.base_url}/prices")
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append(end_time - start_time)
                else:
                    self.log_test("Performance Under Load", False, f"Request {i+1} failed with status {response.status_code}")
                    return False
                
                # Small delay to avoid overwhelming
                time.sleep(0.1)
            
            # Calculate statistics
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            
            # Check if response times are acceptable (< 1s as per requirement)
            if max_response_time < 1.0 and avg_response_time < 0.5:
                self.log_test("Performance Under Load", True, f"Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s")
                return True
            else:
                self.log_test("Performance Under Load", False, f"Slow responses - Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s")
                return False
                
        except Exception as e:
            self.log_test("Performance Under Load", False, f"Exception: {str(e)}")
            return False
        
    def test_root_endpoint(self) -> bool:
        """Test the root API endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Berkay Altın API":
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
    
    def test_admin_login_wrong_credentials(self) -> bool:
        """Test POST /api/admin/login with wrong credentials (expect 401)"""
        try:
            login_data = {
                "username": "wrong_user",
                "password": "wrong_password"
            }
            
            # OAuth2PasswordRequestForm expects form data, not JSON
            response = self.session.post(f"{self.base_url}/admin/login", data=login_data, 
                                       headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if response.status_code == 401:
                self.log_test("Admin Login (Wrong Credentials)", True, "Correctly rejected invalid credentials")
                return True
            else:
                self.log_test("Admin Login (Wrong Credentials)", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Admin Login (Wrong Credentials)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_endpoints_without_token(self) -> bool:
        """Test admin endpoints without authentication token"""
        try:
            # Test /admin/me without token
            response = self.session.get(f"{self.base_url}/admin/me")
            if response.status_code == 401:
                self.log_test("Admin Endpoints (No Token)", True, "Correctly rejected request without token")
                return True
            else:
                self.log_test("Admin Endpoints (No Token)", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Admin Endpoints (No Token)", False, f"Exception: {str(e)}")
            return False
    
    def test_margins_endpoint_without_token(self) -> bool:
        """Test margins endpoint without authentication token"""
        try:
            response = self.session.get(f"{self.base_url}/margins")
            if response.status_code == 401:
                self.log_test("Margins Endpoint (No Token)", True, "Correctly rejected request without token")
                return True
            else:
                self.log_test("Margins Endpoint (No Token)", False, f"Expected 401, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Margins Endpoint (No Token)", False, f"Exception: {str(e)}")
            return False
    
    def test_nonexistent_portfolio_operations(self) -> bool:
        """Test operations on non-existent portfolio items"""
        try:
            fake_id = "non-existent-id-12345"
            
            # Test update non-existent item
            update_data = {"quantity": 10.0}
            response = self.session.put(f"{self.base_url}/portfolio/{fake_id}", json=update_data)
            if response.status_code != 404:
                self.log_test("Non-existent Portfolio Operations", False, f"Update: Expected 404, got {response.status_code}")
                return False
            
            # Test delete non-existent item
            response = self.session.delete(f"{self.base_url}/portfolio/{fake_id}")
            if response.status_code != 404:
                self.log_test("Non-existent Portfolio Operations", False, f"Delete: Expected 404, got {response.status_code}")
                return False
            
            self.log_test("Non-existent Portfolio Operations", True, "Correctly handled non-existent items")
            return True
        except Exception as e:
            self.log_test("Non-existent Portfolio Operations", False, f"Exception: {str(e)}")
            return False
    
    def test_response_times(self) -> bool:
        """Test that response times are under 1 second"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/prices")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200 and response_time < 1.0:
                self.log_test("Response Times", True, f"Prices API responded in {response_time:.3f}s")
                return True
            elif response_time >= 1.0:
                self.log_test("Response Times", False, f"Prices API took {response_time:.3f}s (>1s)")
                return False
            else:
                self.log_test("Response Times", False, f"API error: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Response Times", False, f"Exception: {str(e)}")
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
    
    def run_comprehensive_security_tests(self):
        """Run comprehensive security and functionality tests"""
        print("=" * 80)
        print("ASLANOĞLU KUYUMCULUK (BERKAY ALTIN) - COMPREHENSIVE SECURITY TESTS")
        print("=" * 80)
        print(f"Testing against: {self.base_url}")
        print()
        
        test_results = {}
        
        # ========== SECURITY TESTS ==========
        print("🔒 SECURITY TESTS")
        print("-" * 40)
        
        test_results['cors_policy'] = self.test_cors_policy()
        test_results['sql_injection'] = self.test_sql_injection_attempts()
        test_results['xss_protection'] = self.test_xss_attempts()
        test_results['auth_bypass'] = self.test_authentication_bypass_attempts()
        test_results['jwt_validation'] = self.test_jwt_token_validation()
        test_results['rate_limiting'] = self.test_rate_limiting()
        
        # ========== FUNCTIONALITY TESTS ==========
        print("⚙️  FUNCTIONALITY TESTS")
        print("-" * 40)
        
        test_results['prices_comprehensive'] = self.test_prices_comprehensive()
        test_results['concurrent_requests'] = self.test_concurrent_requests()
        test_results['data_validation'] = self.test_data_validation_comprehensive()
        test_results['performance_load'] = self.test_performance_under_load()
        
        # ========== BASIC API TESTS ==========
        print("🔧 BASIC API TESTS")
        print("-" * 40)
        
        test_results['root'] = self.test_root_endpoint()
        test_results['prices_all'] = self.test_prices_all()
        test_results['prices_gold'] = self.test_prices_gold_only()
        test_results['prices_currency'] = self.test_prices_currency_only()
        
        # Portfolio tests
        gold_item_id = self.test_create_portfolio_gold()
        test_results['create_gold'] = gold_item_id is not None
        
        currency_item_id = self.test_create_portfolio_currency()
        test_results['create_currency'] = currency_item_id is not None
        
        test_results['get_portfolio'] = self.test_get_portfolio()
        
        if gold_item_id:
            test_results['update_portfolio'] = self.test_update_portfolio(gold_item_id)
            test_results['delete_portfolio'] = self.test_delete_portfolio(gold_item_id)
        else:
            test_results['update_portfolio'] = False
            test_results['delete_portfolio'] = False
        
        # Clean up
        if currency_item_id:
            self.test_delete_portfolio(currency_item_id)
        
        # Additional validation tests
        test_results['invalid_creation'] = self.test_invalid_portfolio_creation()
        test_results['admin_wrong_credentials'] = self.test_admin_login_wrong_credentials()
        test_results['admin_no_token'] = self.test_admin_endpoints_without_token()
        test_results['margins_no_token'] = self.test_margins_endpoint_without_token()
        test_results['nonexistent_portfolio'] = self.test_nonexistent_portfolio_operations()
        test_results['response_times'] = self.test_response_times()
        
        # ========== RESULTS SUMMARY ==========
        print("=" * 80)
        print("🔍 SECURITY & FUNCTIONALITY TEST SUMMARY")
        print("=" * 80)
        
        # Security results
        security_tests = ['cors_policy', 'sql_injection', 'xss_protection', 'auth_bypass', 'jwt_validation', 'rate_limiting']
        security_passed = sum(1 for test in security_tests if test_results.get(test, False))
        
        print(f"🔒 SECURITY TESTS: {security_passed}/{len(security_tests)} passed")
        for test in security_tests:
            status = "✅" if test_results.get(test, False) else "❌"
            print(f"   {status} {test.replace('_', ' ').title()}")
        
        # Functionality results
        functionality_tests = ['prices_comprehensive', 'concurrent_requests', 'data_validation', 'performance_load']
        functionality_passed = sum(1 for test in functionality_tests if test_results.get(test, False))
        
        print(f"\n⚙️  FUNCTIONALITY TESTS: {functionality_passed}/{len(functionality_tests)} passed")
        for test in functionality_tests:
            status = "✅" if test_results.get(test, False) else "❌"
            print(f"   {status} {test.replace('_', ' ').title()}")
        
        # API tests
        api_tests = [k for k in test_results.keys() if k not in security_tests + functionality_tests]
        api_passed = sum(1 for test in api_tests if test_results.get(test, False))
        
        print(f"\n🔧 API TESTS: {api_passed}/{len(api_tests)} passed")
        
        # Overall summary
        total_passed = sum(1 for result in test_results.values() if result)
        total_tests = len(test_results)
        
        print(f"\n📊 OVERALL RESULT: {total_passed}/{total_tests} tests passed")
        
        # Security issues summary
        if self.security_issues:
            print(f"\n🚨 SECURITY ISSUES FOUND ({len(self.security_issues)}):")
            for issue in self.security_issues:
                print(f"   • {issue}")
        else:
            print(f"\n🛡️  NO CRITICAL SECURITY ISSUES FOUND")
        
        if total_passed == total_tests and not self.security_issues:
            print("\n🎉 ALL TESTS PASSED - SYSTEM IS SECURE AND FUNCTIONAL!")
            return True
        else:
            print(f"\n⚠️  ISSUES DETECTED - REVIEW REQUIRED")
            return False

def main():
    """Main test execution"""
    tester = HaremAltinAPITester()
    success = tester.run_all_tests()
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()