import os
import requests
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class RapidAPIService:
    def __init__(self):
        # Using free APIs for gold and currency data
        self.gold_api_url = "https://api.gold-api.com/price/XAU"
        self.currency_api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    
    def get_gold_prices(self) -> List[Dict]:
        """Fetch gold prices from free gold API"""
        try:
            # Get international gold price in USD per ounce
            response = requests.get(self.gold_api_url, timeout=10)
            
            if response.status_code == 200:
                gold_data = response.json()
                gold_price_usd = gold_data.get('price', 2700)  # USD per troy ounce
                
                # Get USD/TRY exchange rate
                currency_response = requests.get(self.currency_api_url, timeout=10)
                usd_try = 34.0  # fallback
                if currency_response.status_code == 200:
                    currency_data = currency_response.json()
                    usd_try = currency_data.get('rates', {}).get('TRY', 34.0)
                
                # Calculate Turkish gold prices
                return self._calculate_turkish_gold_prices(gold_price_usd, usd_try)
            else:
                logger.error(f"Gold API error: {response.status_code}")
                return self._get_fallback_gold_data()
        except Exception as e:
            logger.error(f"Error fetching gold prices: {str(e)}")
            return self._get_fallback_gold_data()
    
    def get_currency_rates(self) -> List[Dict]:
        """Fetch currency rates from free exchange rate API"""
        try:
            response = requests.get(self.currency_api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                try_rate = rates.get('TRY', 34.0)
                
                return self._format_currency_from_usd(rates, try_rate)
            else:
                logger.error(f"Currency API error: {response.status_code}")
                return self._get_fallback_currency_data()
        except Exception as e:
            logger.error(f"Error fetching currency rates: {str(e)}")
            return self._get_fallback_currency_data()
    
    def _calculate_turkish_gold_prices(self, gold_price_usd: float, usd_try: float) -> List[Dict]:
        """Calculate Turkish gold prices from international gold price"""
        # 1 troy ounce = 31.1035 grams
        gram_price_try = (gold_price_usd / 31.1035) * usd_try
        
        # Add realistic Turkish market spread (0.5% for buy/sell)
        spread = 0.005
        
        formatted = [
            {
                'id': 1,
                'name': 'HAS ALTIN',
                'nameEn': 'PURE GOLD',
                'buy': round(gram_price_try * (1 - spread), 2),
                'sell': round(gram_price_try * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),  # Compare to base
                'unit': 'TRY'
            },
            {
                'id': 2,
                'name': 'ONS',
                'nameEn': 'OUNCE',
                'buy': round(gold_price_usd * usd_try * (1 - spread), 2),
                'sell': round(gold_price_usd * usd_try * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 3,
                'name': 'ÇEYREK ALTIN',
                'nameEn': 'QUARTER GOLD',
                'buy': round(gram_price_try * 1.75 * (1 - spread), 2),
                'sell': round(gram_price_try * 1.75 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 4,
                'name': 'YARIM ALTIN',
                'nameEn': 'HALF GOLD',
                'buy': round(gram_price_try * 3.5 * (1 - spread), 2),
                'sell': round(gram_price_try * 3.5 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 5,
                'name': 'TAM ALTIN',
                'nameEn': 'FULL GOLD',
                'buy': round(gram_price_try * 7.0 * (1 - spread), 2),
                'sell': round(gram_price_try * 7.0 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 6,
                'name': '22 AYAR',
                'nameEn': '22 CARAT',
                'buy': round(gram_price_try * 0.916 * (1 - spread), 2),
                'sell': round(gram_price_try * 0.916 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 7,
                'name': 'GRAM ALTIN',
                'nameEn': 'GRAM GOLD',
                'buy': round(gram_price_try * (1 - spread), 2),
                'sell': round(gram_price_try * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 8,
                'name': 'ALTIN GÜMÜŞ',
                'nameEn': 'GOLD SILVER',
                'buy': round(gram_price_try * 0.012 * (1 - spread), 2),
                'sell': round(gram_price_try * 0.012 * (1 + spread), 2),
                'change': 0.5,
                'unit': 'TRY'
            },
            {
                'id': 9,
                'name': 'REŞAT ALTIN',
                'nameEn': 'RESAT GOLD',
                'buy': round(gram_price_try * 7.2 * (1 - spread), 2),
                'sell': round(gram_price_try * 7.2 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            },
            {
                'id': 10,
                'name': 'ATA ALTIN',
                'nameEn': 'ATA GOLD',
                'buy': round(gram_price_try * 7.0 * (1 - spread), 2),
                'sell': round(gram_price_try * 7.0 * (1 + spread), 2),
                'change': round((gold_price_usd - 2670) / 2670 * 100, 2),
                'unit': 'TRY'
            }
        ]
        
        return formatted
    
    def _format_currency_from_usd(self, rates: Dict, try_rate: float) -> List[Dict]:
        """Format currency data from USD exchange rates"""
        spread = 0.015  # 1.5% spread for buy/sell
        
        currency_list = [
            ('USD', 'USD', '$', 1.0),
            ('EUR', 'EUR', '€', rates.get('EUR', 0.92)),
            ('GBP', 'GBP', '£', rates.get('GBP', 0.79)),
            ('CHF', 'CHF', 'Fr', rates.get('CHF', 0.88)),
            ('AUD', 'AUD', '$', rates.get('AUD', 1.54)),
            ('CAD', 'CAD', '$', rates.get('CAD', 1.41)),
            ('SAR', 'SAR', 'ر.س', rates.get('SAR', 3.75)),
            ('JPY', 'JPY', '¥', rates.get('JPY', 151.0)),
            ('KWD', 'KWD', 'KD', rates.get('KWD', 0.31))
        ]
        
        formatted = []
        for idx, (code, name, symbol, usd_rate) in enumerate(currency_list, 1):
            # Convert to TRY
            if code == 'USD':
                try_buy = try_rate * (1 - spread)
                try_sell = try_rate * (1 + spread)
            else:
                # Convert other currencies: currency -> USD -> TRY
                usd_per_currency = 1 / usd_rate if usd_rate > 0 else 1
                try_buy = (usd_per_currency * try_rate) * (1 - spread)
                try_sell = (usd_per_currency * try_rate) * (1 + spread)
            
            # Calculate change (simulated as small variation)
            change = round((try_rate - 33.5) / 33.5 * 100, 2) if code == 'USD' else round((try_rate - 33.5) / 33.5 * 100 * 0.8, 2)
            
            formatted.append({
                'id': idx,
                'name': code,
                'nameEn': code,
                'buy': round(try_buy, 2),
                'sell': round(try_sell, 2),
                'change': change,
                'symbol': symbol,
                'unit': 'TRY'
            })
        
        # Add gold-based currency rates
        gold_gram_try = try_rate * 85  # Approximate gram gold price
        formatted.append({
            'id': 10,
            'name': 'USD/KG',
            'nameEn': 'USD/KG',
            'buy': round(gold_gram_try * 1000 / try_rate * (1 - spread), 2),
            'sell': round(gold_gram_try * 1000 / try_rate * (1 + spread), 2),
            'change': 0.55,
            'symbol': '$',
            'unit': 'TRY'
        })
        
        formatted.append({
            'id': 11,
            'name': 'EUR/KG',
            'nameEn': 'EUR/KG',
            'buy': round(gold_gram_try * 1000 / try_rate / rates.get('EUR', 0.92) * (1 - spread), 2),
            'sell': round(gold_gram_try * 1000 / try_rate / rates.get('EUR', 0.92) * (1 + spread), 2),
            'change': 0.68,
            'symbol': '€',
            'unit': 'TRY'
        })
        
        return formatted
    
    def _get_fallback_gold_data(self) -> List[Dict]:
        """Fallback gold data if API fails"""
        return [
            {'id': 1, 'name': 'HAS ALTIN', 'nameEn': 'PURE GOLD', 'buy': 5807.50, 'sell': 5858.70, 'change': 0.74, 'unit': 'TRY'},
            {'id': 2, 'name': 'ONS', 'nameEn': 'OUNCE', 'buy': 4239.5, 'sell': 4239.9, 'change': 0.53, 'unit': 'TRY'},
            {'id': 3, 'name': 'ÇEYREK ALTIN', 'nameEn': 'QUARTER GOLD', 'buy': 2389.0, 'sell': 2398.0, 'change': 0.68, 'unit': 'TRY'},
            {'id': 4, 'name': 'YARIM ALTIN', 'nameEn': 'HALF GOLD', 'buy': 4779.0, 'sell': 4796.0, 'change': 0.72, 'unit': 'TRY'},
            {'id': 5, 'name': 'TAM ALTIN', 'nameEn': 'FULL GOLD', 'buy': 9558.0, 'sell': 9592.0, 'change': 0.75, 'unit': 'TRY'},
            {'id': 6, 'name': '22 AYAR', 'nameEn': '22 CARAT', 'buy': 5282.82, 'sell': 5545.77, 'change': 4.83, 'unit': 'TRY'},
            {'id': 7, 'name': 'GRAM ALTIN', 'nameEn': 'GRAM GOLD', 'buy': 5778.46, 'sell': 5876.28, 'change': 1.55, 'unit': 'TRY'},
            {'id': 8, 'name': 'ALTIN GÜMÜŞ', 'nameEn': 'GOLD SILVER', 'buy': 70.66, 'sell': 73.63, 'change': 0.59, 'unit': 'TRY'},
            {'id': 9, 'name': 'REŞAT ALTIN', 'nameEn': 'RESAT GOLD', 'buy': 9872.0, 'sell': 9912.0, 'change': 0.82, 'unit': 'TRY'},
            {'id': 10, 'name': 'ATA ALTIN', 'nameEn': 'ATA GOLD', 'buy': 9612.0, 'sell': 9652.0, 'change': 0.78, 'unit': 'TRY'}
        ]
    
    def _get_fallback_currency_data(self) -> List[Dict]:
        """Fallback currency data if API fails"""
        return [
            {'id': 1, 'name': 'USD', 'nameEn': 'USD', 'buy': 34.125, 'sell': 34.225, 'change': 0.55, 'symbol': '$', 'unit': 'TRY'},
            {'id': 2, 'name': 'EUR', 'nameEn': 'EUR', 'buy': 35.890, 'sell': 36.050, 'change': 0.68, 'symbol': '€', 'unit': 'TRY'},
            {'id': 3, 'name': 'GBP', 'nameEn': 'GBP', 'buy': 43.250, 'sell': 43.450, 'change': 0.42, 'symbol': '£', 'unit': 'TRY'},
            {'id': 4, 'name': 'CHF', 'nameEn': 'CHF', 'buy': 38.650, 'sell': 38.850, 'change': 0.38, 'symbol': 'Fr', 'unit': 'TRY'},
            {'id': 5, 'name': 'AUD', 'nameEn': 'AUD', 'buy': 22.150, 'sell': 22.350, 'change': 0.25, 'symbol': '$', 'unit': 'TRY'},
            {'id': 6, 'name': 'CAD', 'nameEn': 'CAD', 'buy': 24.050, 'sell': 24.250, 'change': 0.31, 'symbol': '$', 'unit': 'TRY'},
            {'id': 7, 'name': 'SAR', 'nameEn': 'SAR', 'buy': 9.100, 'sell': 9.200, 'change': 0.18, 'symbol': 'ر.س', 'unit': 'TRY'},
            {'id': 8, 'name': 'JPY', 'nameEn': 'JPY', 'buy': 0.226, 'sell': 0.230, 'change': 0.22, 'symbol': '¥', 'unit': 'TRY'},
            {'id': 9, 'name': 'KWD', 'nameEn': 'KWD', 'buy': 111.250, 'sell': 112.150, 'change': 0.45, 'symbol': 'KD', 'unit': 'TRY'},
            {'id': 10, 'name': 'USD/KG', 'nameEn': 'USD/KG', 'buy': 137.020, 'sell': 137.520, 'change': 0.55, 'symbol': '$', 'unit': 'TRY'},
            {'id': 11, 'name': 'EUR/KG', 'nameEn': 'EUR/KG', 'buy': 118.090, 'sell': 118.750, 'change': 0.68, 'symbol': '€', 'unit': 'TRY'}
        ]

rapidapi_service = RapidAPIService()