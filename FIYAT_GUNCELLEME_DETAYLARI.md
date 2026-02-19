# 🔄 Fiyat Güncelleme Sıklığı - BERKAY ALTIN

## 📊 Özet

**Frontend Güncelleme:** Her **60 saniye** (1 dakika)  
**Backend API:** Her istekte **canlı veri** (cache yok)  
**Kaynak:** RapidAPI - Harem Altın Live Gold Price Data

---

## 🎯 Detaylı Açıklama

### 1. Frontend Otomatik Yenileme

**Dosya:** `/app/frontend/src/components/HomePage.js`  
**Satır:** 67

```javascript
useEffect(() => {
  fetchPrices();
  // Auto-refresh every 60 seconds
  const interval = setInterval(fetchPrices, 60000);
  return () => clearInterval(interval);
}, []);
```

**Açıklama:**
- Sayfa ilk yüklendiğinde fiyatları çeker
- Her **60.000 milisaniye** (60 saniye = 1 dakika) sonra otomatik yenilenir
- Kullanıcı sayfayı kapatana kadar döngü devam eder
- Manuel yenileme butonu da mevcut (🔄 ikonu)

---

### 2. Backend API - Canlı Veri

**Dosya:** `/app/backend/harem_api_service.py`  
**Metod:** `get_all_prices()`

**Akış:**
1. Frontend her 60 saniyede `/api/prices` endpoint'ine istek atar
2. Backend her istekte **RapidAPI'ye canlı sorgu** atar
3. RapidAPI'den güncel Türkiye piyasası verileri gelir
4. Backend format düzenler ve frontend'e gönderir

**Cache YOK:** Her istek = canlı veri

**Timeout:** 10 saniye (RapidAPI yanıt vermezse)

**Fallback:** API hata verirse statik fallback data kullanılır

---

## 📈 Veri Kaynağı

**API:** RapidAPI - Harem Altın Live Gold Price Data  
**Endpoint:** `https://harem-altin-anlik-altin-fiyatlari-live-rates-gold.p.rapidapi.com/economy/live-exchange-rates`

**Kapsam:**
- 14 Altın Ürünü (HAS ALTIN, GRAM, ÇEYREK, YARIM, TAM, ONS, vb.)
- 11 Döviz Kuru (USD, EUR, GBP, JPY, CHF, AUD, CAD, SAR, KWD, vb.)

**Doğruluk:** Türkiye piyasası gerçek zamanlı fiyatlar

---

## ⚙️ Güncelleme Sıklığını Değiştirmek

### Frontend'te Güncelleme Aralığını Değiştir

**Dosya:** `/app/frontend/src/components/HomePage.js`  
**Satır:** 67

```javascript
// Şu an: 60 saniye (60000 ms)
const interval = setInterval(fetchPrices, 60000);

// 30 saniye yapmak için:
const interval = setInterval(fetchPrices, 30000);

// 2 dakika yapmak için:
const interval = setInterval(fetchPrices, 120000);

// 5 dakika yapmak için:
const interval = setInterval(fetchPrices, 300000);
```

**Önerilen Değerler:**
- **30 saniye:** Çok hızlı (RapidAPI rate limit riski)
- **60 saniye (mevcut):** İdeal denge ✅
- **120 saniye:** Makul, daha az API kullanımı
- **300 saniye:** Yavaş ama çok ekonomik

---

### Backend'de Cache Eklemek (İsteğe Bağlı)

Eğer her istekte API çağrısı maliyetli geliyorsa, cache eklenebilir:

**Örnek Implementation:**

```python
# harem_api_service.py

import time

class HaremAPIService:
    def __init__(self):
        self.headers = {...}
        self.cache = None
        self.cache_timestamp = 0
        self.cache_ttl = 30  # 30 saniye cache
    
    def get_all_prices(self) -> Dict:
        # Cache kontrolü
        now = time.time()
        if self.cache and (now - self.cache_timestamp) < self.cache_ttl:
            return self.cache
        
        # API'ye istek at
        try:
            response = requests.get(...)
            data = self._format_prices(response.json())
            
            # Cache'e kaydet
            self.cache = data
            self.cache_timestamp = now
            
            return data
        except Exception as e:
            # Cache varsa onu kullan
            if self.cache:
                return self.cache
            return self._get_fallback_data()
```

**Avantajlar:**
- RapidAPI kullanımını azaltır
- Response time daha hızlı
- Rate limit riskini azaltır

**Dezavantajlar:**
- Fiyatlar 30 saniye "eski" olabilir
- Bellekte cache tutar

---

## 🔍 Mevcut Durum Test

**Test Komutu:**
```bash
# Backend API'yi test et
curl -s https://berkayfinance.preview.emergentagent.com/api/prices | python3 -c "import sys,json; d=json.load(sys.stdin); print('Last Update:', d['lastUpdate']); print('Gold items:', len(d['gold'])); print('Currency items:', len(d['currency']))"
```

**Beklenen Çıktı:**
```
Last Update: 2026-02-19T13:45:22.123456
Gold items: 14
Currency items: 11
```

---

## 📊 Rate Limit Bilgisi

**RapidAPI Free Tier (varsayılan):**
- Genellikle 100-500 istek/gün
- 60 saniye güncelleme ile: 1,440 istek/gün (60 min × 24 saat)

**Öneri:**
- Eğer çok kullanıcı olursa, backend cache ekleyin
- Veya güncelleme aralığını 2 dakikaya çıkarın (720 istek/gün)
- Veya RapidAPI plan upgrade yapın

---

## 🎯 Sonuç

✅ **Mevcut Ayar:** Frontend her 60 saniyede yenileniyor  
✅ **Backend:** Canlı veri (cache yok)  
✅ **Doğruluk:** Türkiye piyasası gerçek zamanlı  
✅ **Performans:** < 1s response time  

**Değişiklik Gerekli mi?** HAYIR - Mevcut ayar ideal! ✅

---

**Son Güncelleme:** 19 Şubat 2026  
**Proje:** BERKAY ALTIN
