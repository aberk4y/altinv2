import os
import requests
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY', '')
RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST', "harem-altin-anlik-altin-fiyatlari-live-rates-gold.p.rapidapi.com")

class HaremAPIService:
    def __init__(self):
        self.headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        self.base_url = f"https://{RAPIDAPI_HOST}"
    
    def get_all_prices(self) -> Dict:
        """Fetch all gold and currency prices from Harem Altın API"""
        try:
            url = f"{self.base_url}/economy/live-exchange-rates"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    return self._format_prices(data.get('data', []))
                else:
                    logger.error(f"Harem API error: No data field")
                    return self._get_fallback_data()
            else:
                logger.error(f"Harem API HTTP error: {response.status_code}")
                return self._get_fallback_data()
        except Exception as e:
            logger.error(f"Error fetching Harem prices: {str(e)}")
            return self._get_fallback_data()
    
    def _format_prices(self, raw_data: List[Dict]) -> Dict:
        """Format Harem API data into gold and currency categories"""
        gold_items = []
        currency_items = []
        
        # Gold price mappings (New API codes -> (Name TR, Name EN))
        gold_mapping = {
            'altintry': ('HAS ALTIN', 'PURE GOLD'),
            'onstry': ('ONS', 'OUNCE'),
            'gramaltin': ('GRAM ALTIN', 'GRAM GOLD'),
            '22ayar': ('22 AYAR', '22 CARAT'),
            '14ayar': ('14 AYAR', '14 CARAT'),
            'altingumus': ('ALTIN GÜMÜŞ', 'GOLD SILVER'),
            'ceyrekaltin': ('ÇEYREK ALTIN', 'QUARTER GOLD'),
            'yarimaltin': ('YARIM ALTIN', 'HALF GOLD'),
            'tekaltin': ('TAM ALTIN', 'FULL GOLD'),
            'ata': ('ATA ALTIN', 'ATA GOLD'),
            'ceyrekaltineski': ('ESKİ ÇEYREK', 'OLD QUARTER'),
            'yarimaltineski': ('ESKİ YARIM', 'OLD HALF'),
            'tekaltineski': ('ESKİ TAM', 'OLD FULL'),
            'ataeski': ('ESKİ ATA', 'OLD ATA')
        }
        
        # Currency mappings
        currency_mapping = {
            'USDTRY': ('USD', 'USD', '$'),
            'EURTRY': ('EUR', 'EUR', '€'),
            'GBPTRY': ('GBP', 'GBP', '£'),
            'CHFTRY': ('CHF', 'CHF', 'Fr'),
            'AUDTRY': ('AUD', 'AUD', '$'),
            'CADTRY': ('CAD', 'CAD', '$'),
            'SARTRY': ('SAR', 'SAR', 'ر.س'),
            'JPYTRY': ('JPY', 'JPY', '¥'),
            'KWDTRY': ('KWD', 'KWD', 'KD'),
            'USDKG': ('USD/KG', 'USD/KG', '$'),
            'EURKG': ('EUR/KG', 'EUR/KG', '€')
        }
        
        gold_counter = 1
        currency_counter = 1
        
        for item in raw_data:
            code = item.get('currencyCode', '')
            # Try both exact match and lowercase
            key = code
            if key not in gold_mapping and key.lower() in gold_mapping:
                key = key.lower()
            
            buy = float(item.get('buy', 0))
            sell = float(item.get('sell', 0))
            change = float(item.get('changeRate', 0))
            
            # Check if it's a gold item
            if key in gold_mapping:
                name_tr, name_en = gold_mapping[key]
                gold_items.append({
                    'id': gold_counter,
                    'name': name_tr,
                    'nameEn': name_en,
                    'buy': buy,
                    'sell': sell,
                    'change': change,
                    'unit': 'TRY'
                })
                gold_counter += 1
            
            # Check if it's a currency item
            elif key in currency_mapping:
                name_tr, name_en, symbol = currency_mapping[key]
                currency_items.append({
                    'id': currency_counter,
                    'name': name_tr,
                    'nameEn': name_en,
                    'buy': buy,
                    'sell': sell,
                    'change': change,
                    'symbol': symbol,
                    'unit': 'TRY'
                })
                currency_counter += 1
        
        # Sort or filter if needed, but the loop preserves API order generally
        # We might want to ensure specific items are present or fallback?
        # For now, trusted the API list.
        
        return {
            'gold': gold_items,
            'currency': currency_items
        }
    
    def _get_fallback_data(self) -> Dict:
        """Fallback data if API fails"""
        return {
            'gold': [
                {'id': 1, 'name': 'HAS ALTIN', 'nameEn': 'PURE GOLD', 'buy': 5807.50, 'sell': 5858.70, 'change': 0.74, 'unit': 'TRY'},
                {'id': 2, 'name': 'ONS', 'nameEn': 'OUNCE', 'buy': 4239.5, 'sell': 4239.9, 'change': 0.53, 'unit': 'TRY'},
                {'id': 3, 'name': 'ÇEYREK ALTIN', 'nameEn': 'QUARTER GOLD', 'buy': 2389.0, 'sell': 2398.0, 'change': 0.68, 'unit': 'TRY'},
                {'id': 4, 'name': 'YARIM ALTIN', 'nameEn': 'HALF GOLD', 'buy': 4779.0, 'sell': 4796.0, 'change': 0.72, 'unit': 'TRY'},
                {'id': 5, 'name': 'TAM ALTIN', 'nameEn': 'FULL GOLD', 'buy': 9558.0, 'sell': 9592.0, 'change': 0.75, 'unit': 'TRY'},
                {'id': 6, 'name': '22 AYAR', 'nameEn': '22 CARAT', 'buy': 5282.82, 'sell': 5545.77, 'change': 4.83, 'unit': 'TRY'},
                {'id': 7, 'name': 'GRAM ALTIN', 'nameEn': 'GRAM GOLD', 'buy': 5778.46, 'sell': 5876.28, 'change': 1.55, 'unit': 'TRY'},
                {'id': 8, 'name': 'ALTIN GÜMÜŞ', 'nameEn': 'GOLD SILVER', 'buy': 70.66, 'sell': 73.63, 'change': 0.59, 'unit': 'TRY'},
                {'id': 9, 'name': 'ESKİ ÇEYREK', 'nameEn': 'OLD QUARTER', 'buy': 9320.0, 'sell': 9493.0, 'change': 0.82, 'unit': 'TRY'},
                {'id': 10, 'name': 'ATA ALTIN', 'nameEn': 'ATA GOLD', 'buy': 9612.0, 'sell': 9652.0, 'change': 0.78, 'unit': 'TRY'}
            ],
            'currency': [
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
        }

harem_api_service = HaremAPIService()
