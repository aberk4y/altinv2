# BERKAY ALTIN - Detaylı Proje Dökümanı

## 📋 İÇİNDEKİLER
1. [Proje Özeti](#proje-özeti)
2. [Teknoloji Stack](#teknoloji-stack)
3. [Mevcut Proje Yapısı](#mevcut-proje-yapısı)
4. [Şimdiye Kadar Yapılanlar (Detaylı)](#şimdiye-kadar-yapılanlar)
5. [Bundan Sonra Yapılacaklar (Adım Adım)](#bundan-sonra-yapılacaklar)
6. [Teknik Detaylar ve Özel Notlar](#teknik-detaylar)

---

## PROJE ÖZETİ

### Proje Adı
**BERKAY ALTIN** - Mobil Altın ve Döviz Fiyat Takip Uygulaması

### Proje Amacı
"Harem Altın" uygulamasının bir klon'u olarak, kullanıcıların canlı altın ve döviz fiyatlarını takip edebileceği, dönüştürme yapabileceği ve portföy yönetimi yapabileceği mobil bir uygulama geliştirmek.

### Hedef Platform
- iOS (Apple App Store)
- Android (Google Play Store)

### Temel Özellikler
1. **Canlı Fiyat Gösterimi**: Türkiye piyasasından gerçek zamanlı altın ve döviz fiyatları
2. **Dil Desteği**: Türkçe ve İngilizce
3. **Dönüştürücü**: Altın/Döviz birimi dönüşüm aracı
4. **Portföy Yönetimi**: Kullanıcıların altın/döviz varlıklarını takip edebilmesi
5. **Admin Panel**: Kar marjı yönetimi için web tabanlı yönetim paneli
6. **Responsive Tasarım**: Mobil cihazlara optimize edilmiş arayüz (375px genişlik)

### Proje Sahibi Bilgileri
- **GitHub Repository**: https://github.com/aberk4y/berkay-altin
- **RapidAPI Key**: `1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4`
- **API Endpoint**: `harem-altin-live-gold-price-data.p.rapidapi.com`

---

## TEKNOLOJİ STACK

### Frontend
- **Framework**: React 18.x
- **Build Tool**: Create React App
- **Styling**: 
  - Tailwind CSS (utility-first CSS framework)
  - Shadcn UI (React component library)
- **Routing**: react-router-dom v6
- **State Management**: React useState/useEffect hooks
- **HTTP Client**: Fetch API
- **Package Manager**: Yarn (NOT npm - kritik!)
- **Dil Desteği**: Custom translation object (TR/EN)

### Backend
- **Framework**: FastAPI (Python 3.x)
- **ASGI Server**: Uvicorn
- **HTTP Client**: httpx (async HTTP requests)
- **Validation**: Pydantic models
- **CORS**: fastapi.middleware.cors
- **Environment Variables**: python-dotenv

### Database
- **Database**: MongoDB (local instance)
- **Driver**: Motor (async MongoDB driver for Python)
- **Connection**: mongodb://localhost:27017

### DevOps & Infrastructure
- **Process Manager**: Supervisor
- **Web Server**: Nginx (reverse proxy)
- **Backend Port**: 8001 (internal: 0.0.0.0:8001)
- **Frontend Port**: 3000 (internal: localhost:3000)
- **MongoDB Port**: 27017
- **Hot Reload**: Frontend ve Backend'de aktif

### External APIs
- **API Provider**: RapidAPI
- **API Name**: Harem Altın Live Gold Price Data
- **API Host**: harem-altin-live-gold-price-data.p.rapidapi.com
- **Endpoint**: `/api/doviz`
- **Method**: GET
- **Rate Limit**: Bilinmiyor (ücretsiz plan)

### Gelecekte Kullanılacak Teknolojiler

#### Mobil App Build (Capacitor)
- **Framework**: Capacitor 5.x/6.x (by Ionic)
- **Neden Capacitor?**: React uygulamasını native iOS/Android'e dönüştürür
- **CLI Tool**: `@capacitor/cli`
- **Platform Packages**:
  - `@capacitor/android` (Android için)
  - `@capacitor/ios` (iOS için)
- **Plugins**:
  - `@capacitor/splash-screen` (Açılış logosu)
  - `@capacitor/status-bar` (Durum çubuğu yönetimi)
  - `@capacitor/app` (App lifecycle events)

#### Admin Panel için Eklenecekler
- **Authentication**: JWT (JSON Web Tokens)
  - Library: `python-jose[cryptography]`
- **Password Hashing**: bcrypt
  - Library: `passlib[bcrypt]`
- **Form Validation**: Backend'de Pydantic, Frontend'de custom validation
- **Session Management**: JWT token with expiry

#### Deployment
- **Backend Hosting**: TBD (Heroku, Railway, DigitalOcean, AWS vb.)
- **Frontend/Admin Hosting**: TBD (Vercel, Netlify, vb. veya backend ile birlikte)
- **Database**: MongoDB Atlas (cloud) veya self-hosted
- **Domain**: TBD (örn: berkayaltin.com)
- **SSL**: Let's Encrypt (HTTPS için)

---

## MEVCUT PROJE YAPISI

### Dizin Ağacı
```
/app
├── backend/
│   ├── .env                          # Environment variables
│   ├── server.py                     # Ana FastAPI uygulaması
│   ├── harem_api_service.py          # Harem API entegrasyon servisi
│   ├── rapidapi_service.py           # Eski API servisi (artık kullanılmıyor, silinebilir)
│   ├── models.py                     # Pydantic data models
│   ├── requirements.txt              # Python dependencies
│   └── tests/                        # Test dosyaları (henüz oluşturulmadı)
│
├── frontend/
│   ├── public/
│   │   ├── index.html                # Ana HTML (title: "BERKAY ALTIN")
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js           # Ana sayfa (fiyat panosu)
│   │   │   ├── ConverterPage.js      # Dönüştürücü sayfası
│   │   │   ├── PortfolioPage.js      # Portföy yönetimi sayfası
│   │   │   ├── BottomNav.js          # Alt navigasyon bar
│   │   │   └── ui/                   # Shadcn UI components
│   │   │       ├── button.jsx
│   │   │       ├── card.jsx
│   │   │       ├── input.jsx
│   │   │       ├── select.jsx
│   │   │       ├── tabs.jsx
│   │   │       └── ... (diğer shadcn componentler)
│   │   ├── services/
│   │   │   └── api.js                # API call helper functions
│   │   ├── App.js                    # Ana router component
│   │   ├── App.css                   # Global styles
│   │   ├── index.js                  # React entry point
│   │   └── index.css                 # Tailwind imports
│   ├── package.json                  # Node dependencies
│   ├── yarn.lock                     # Yarn lock file
│   ├── tailwind.config.js            # Tailwind configuration
│   └── postcss.config.js             # PostCSS configuration
│
├── contracts.md                      # API contracts dökümanı
├── test_result.md                    # Test sonuçları
└── PROJE_DETAYLI_DOKUMAN.md         # Bu dosya
```

### Environment Variables

#### Backend (.env)
```bash
# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=berkay_altin_db

# RapidAPI Credentials
RAPIDAPI_KEY=1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4
RAPIDAPI_HOST=harem-altin-live-gold-price-data.p.rapidapi.com
```

#### Frontend (.env)
```bash
REACT_APP_BACKEND_URL=<production-url>
# Development'ta buraya production URL yazılmış olmalı
# Kubernetes ingress otomatik olarak routing yapıyor
```

### Supervisor Konfigürasyonu
Backend ve Frontend, Supervisor tarafından yönetiliyor:
- **Backend**: Uvicorn ile 0.0.0.0:8001'de çalışıyor
- **Frontend**: React dev server 3000'de çalışıyor
- **Hot Reload**: Kod değişikliklerinde otomatik yeniden yükleme aktif
- **Restart Komutu**: `sudo supervisorctl restart backend` veya `sudo supervisorctl restart frontend`
- **Status Kontrol**: `sudo supervisorctl status`

### Önemli Notlar
1. **Package Manager**: SADECE `yarn` kullanılmalı, `npm` kullanımı breaking change yaratır
2. **Python Packages**: requirements.txt güncellenirken önce `pip install <package>` sonra `pip freeze > /app/backend/requirements.txt`
3. **Environment Variables**: ASLA hardcode edilmemeli, her zaman .env'den okunmalı
4. **API Prefix**: Tüm backend endpoint'leri `/api` prefix'i ile başlamalı (Kubernetes ingress kuralı)

---

## ŞİMDİYE KADAR YAPILANLAR

### Faz 0: Proje Kurulumu ve Temel Geliştirme (TAMAMLANDI ✅)

#### 1. Proje İnisiyalizasyonu
**Yapılan:**
- React + FastAPI + MongoDB template'den başlandı
- Proje ismi "BERKAY ALTIN" olarak belirlendi
- GitHub repository oluşturuldu: https://github.com/aberk4y/berkay-altin

**Teknik Detaylar:**
- Create React App ile frontend oluşturuldu
- FastAPI backend template'i kullanıldı
- MongoDB local instance konfigüre edildi

#### 2. Harem Altın API Entegrasyonu
**Sorun:**
- İlk başta genel bir altın API kullanılmaya çalışıldı
- Fiyatlar Türkiye piyasası ile uyuşmuyordu
- Kullanıcı özel bir RapidAPI key'i sağladı

**Çözüm:**
- Yeni bir servis dosyası oluşturuldu: `harem_api_service.py`
- API Endpoint: `https://harem-altin-live-gold-price-data.p.rapidapi.com/api/doviz`
- Request headers'a özel key eklendi

**Kod Örneği (harem_api_service.py):**
```python
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

async def get_harem_prices():
    url = f"https://{RAPIDAPI_HOST}/api/doviz"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        # Data parsing logic here
        # ...
        
        return {
            "lastUpdate": datetime.now().isoformat(),
            "gold": gold_list,
            "currency": currency_list
        }
```

#### 3. Backend API Endpoint'lerinin Oluşturulması
**Oluşturulan Endpoint'ler:**

##### `/api/prices` (GET)
- Canlı altın ve döviz fiyatlarını döner
- Response structure:
```json
{
  "lastUpdate": "2025-12-01T22:28:31.489116",
  "gold": [
    {
      "id": 1,
      "name": "14 AYAR",
      "nameEn": "14 CARAT",
      "buy": 3188.82,
      "sell": 4303.97,
      "change": 34.84,
      "unit": "TRY"
    },
    // ... diğer altın ürünleri
  ],
  "currency": [
    {
      "id": 1,
      "name": "USD",
      "nameEn": "USD",
      "buy": 42.3,
      "sell": 42.72,
      "change": 1.21,
      "symbol": "$",
      "unit": "TRY"
    },
    // ... diğer dövizler
  ]
}
```

##### `/api/portfolio` (GET)
- Kullanıcının portföyündeki öğeleri listeler
- MongoDB'den `portfolio_items` collection'ını okur
- Response: Portfolio item array

##### `/api/portfolio` (POST)
- Yeni portföy öğesi ekler
- Request body:
```json
{
  "name": "Gram Altın",
  "amount": 10.5,
  "value": 60000
}
```

##### `/api/portfolio/{id}` (DELETE)
- Belirtilen ID'ye sahip portföy öğesini siler

**Backend server.py Ana Yapısı:**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from uuid import uuid4

# IMPORTANT: Load env before imports that use env vars
load_dotenv()

from harem_api_service import get_harem_prices

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

@app.get("/api/prices")
async def get_prices():
    try:
        prices = await get_harem_prices()
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ... diğer endpoint'ler
```

#### 4. Frontend Sayfalarının Geliştirilmesi

##### 4.1 HomePage.js (Ana Sayfa / Fiyat Panosu)
**Özellikler:**
- Canlı altın ve döviz fiyatlarını gösterir
- Tab'ler ile altın ve döviz arasında geçiş
- Her ürün için:
  - İsim (TR/EN dil desteği)
  - Alış fiyatı
  - Satış fiyatı
  - Değişim yüzdesi (renkli: yeşil pozitif, kırmızı negatif)
- Otomatik yenileme (her 30 saniyede bir)
- Loading state
- Error handling

**Kullanılan Componentler:**
- Shadcn `Tabs`, `Card`, `Button`
- Custom `BottomNav`

**Kod Snippet:**
```javascript
import { useState, useEffect } from 'react';
import { getPrices } from '../services/api';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Card } from './ui/card';

export default function HomePage() {
  const [prices, setPrices] = useState(null);
  const [loading, setLoading] = useState(true);
  const [language, setLanguage] = useState('tr');

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const data = await getPrices();
        setPrices(data);
      } catch (error) {
        console.error('Fiyatlar alınamadı:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 30000); // 30 saniye
    return () => clearInterval(interval);
  }, []);

  // ... render logic
}
```

##### 4.2 ConverterPage.js (Dönüştürücü)
**Özellikler:**
- Altın ve döviz birimlerini birbirine dönüştürme
- Dropdown'dan ürün seçimi
- Miktar girişi
- Anlık hesaplama
- Sonuç gösterimi (alış ve satış fiyatları)

**Kullanılan Componentler:**
- Shadcn `Card`, `Select`, `Input`, `Button`

**Dönüşüm Mantığı:**
```javascript
const handleConvert = () => {
  if (!fromProduct || !toProduct || !amount) return;

  const fromRate = fromProduct.buy; // Alış fiyatı
  const toRate = toProduct.sell; // Satış fiyatı
  
  const result = (amount * fromRate) / toRate;
  setConvertedAmount(result.toFixed(4));
};
```

##### 4.3 PortfolioPage.js (Portföy Yönetimi)
**Özellikler:**
- Kullanıcının portföyündeki altın/döviz varlıklarını listeler
- Yeni varlık ekleme formu
- Varlık silme özelliği
- Toplam portföy değeri hesaplama
- Her varlık için:
  - İsim
  - Miktar
  - Toplam değer (TRY)

**CRUD Operasyonları:**
- **Create**: Form ile yeni item ekleme
- **Read**: Sayfa yüklendiğinde portfolio items'ları çekme
- **Delete**: Silme butonu ile item'ı kaldırma

**API Calls:**
```javascript
// Fetch portfolio
const fetchPortfolio = async () => {
  const data = await getPortfolio();
  setPortfolioItems(data);
};

// Add item
const handleAddItem = async () => {
  await addPortfolioItem({
    name: newItem.name,
    amount: parseFloat(newItem.amount),
    value: parseFloat(newItem.value)
  });
  fetchPortfolio();
};

// Delete item
const handleDeleteItem = async (id) => {
  await deletePortfolioItem(id);
  fetchPortfolio();
};
```

##### 4.4 BottomNav.js (Alt Navigasyon)
**Özellikler:**
- Fixed bottom navigation bar
- 3 sayfa arası geçiş: Ana Sayfa, Dönüştürücü, Portföy
- Aktif sayfa vurgusu
- İkonlar ile görsel navigasyon
- Mobil optimizasyon (375px genişlik)

**Routing:**
```javascript
import { Link, useLocation } from 'react-router-dom';

const BottomNav = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Ana Sayfa', icon: '🏠' },
    { path: '/converter', label: 'Çevirici', icon: '🔄' },
    { path: '/portfolio', label: 'Portföy', icon: '💼' }
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t">
      {navItems.map(item => (
        <Link 
          to={item.path}
          className={location.pathname === item.path ? 'active' : ''}
        >
          {item.icon} {item.label}
        </Link>
      ))}
    </nav>
  );
};
```

#### 5. Çok Dilli (TR/EN) Destek Sistemi
**Implementasyon:**
- Her component'te language state'i tutuldu
- Translation object'leri oluşturuldu
- Dil değiştirme butonu eklendi

**Translation Örneği (HomePage.js):**
```javascript
const translations = {
  tr: {
    gold: 'Altın',
    currency: 'Döviz',
    buy: 'Alış',
    sell: 'Satış',
    change: 'Değişim',
    lastUpdate: 'Son Güncelleme'
  },
  en: {
    gold: 'Gold',
    currency: 'Currency',
    buy: 'Buy',
    sell: 'Sell',
    change: 'Change',
    lastUpdate: 'Last Update'
  }
};
```

#### 6. Styling ve UI/UX İyileştirmeleri
**Tailwind CSS Konfigürasyonu:**
- Mobile-first approach (375px genişlik)
- Custom color palette:
  - Primary: Yeşil tonları (#22c55e, #16a34a)
  - Gold accent: Altın sarısı (#fbbf24)
  - Background: Açık gri (#f9fafb)
- Responsive design (sm, md, lg breakpoints)

**Shadcn UI Components:**
- Button: Primary ve secondary variants
- Card: Shadow ve padding ayarları
- Input: Outline ve focus states
- Select: Dropdown styling
- Tabs: Underline active indicator

**Custom CSS (App.css):**
```css
.price-up {
  color: #22c55e;
}

.price-down {
  color: #ef4444;
}

.mobile-container {
  max-width: 375px;
  margin: 0 auto;
}

.fixed-bottom-nav {
  padding-bottom: 80px; /* Bottom nav için boşluk */
}
```

#### 7. Kritik Bug Fix'ler

##### Bug #1: Environment Variables Yüklenmiyor
**Sorun:**
- Backend başlatıldığında RAPIDAPI_KEY bulunamıyordu
- `None` değeri API call'larda hata veriyordu

**Kök Neden:**
- `server.py`'da import sırası yanlıştı
- `harem_api_service.py` import edilmeden önce `load_dotenv()` çağrılmıyordu

**Çözüm:**
```python
# ÖNCE
from dotenv import load_dotenv
load_dotenv()

# SONRA
from harem_api_service import get_harem_prices
```

##### Bug #2: Yanlış Fiyat Hesaplama
**Sorun:**
- API'den gelen fiyat değerleri düzgün parse edilmiyordu
- String olarak gelen değerler float'a dönüştürülmüyordu

**Çözüm:**
```python
# Raw API response
"alis": "3.188,82"
"satis": "4.303,97"

# Parsing function
def parse_price(price_str):
    # Virgülü noktaya çevir, nokta ayırıcılarını kaldır
    return float(price_str.replace('.', '').replace(',', '.'))

buy = parse_price(item.get("alis", "0"))
sell = parse_price(item.get("satis", "0"))
```

##### Bug #3: MongoDB ObjectId Serialization Hatası
**Sorun:**
- MongoDB'den dönen `_id` field'ı JSON serialize edilemiyordu
- FastAPI error response döndürüyordu

**Çözüm:**
```python
# MongoDB query'lerinde _id field'ını exclude et
items = await db.portfolio_items.find({}, {"_id": 0}).to_list(1000)

# Yeni kayıtlarda custom ID kullan
item = {
    "id": str(uuid4()),  # UUID kullan
    "name": name,
    "amount": amount,
    "value": value
}
```

#### 8. Git ve GitHub Entegrasyonu
**Yapılanlar:**
- `.gitignore` oluşturuldu:
  ```
  __pycache__/
  *.pyc
  .env
  node_modules/
  build/
  .DS_Store
  ```
- İlk commit: "Initial commit - BERKAY ALTIN app"
- Tüm feature commit'leri anlamlı mesajlarla yapıldı
- GitHub'a push edildi: https://github.com/aberk4y/berkay-altin
- Branch: `main`

#### 9. Testing (Kısıtlı)
**Yapılan Testler:**
- Manual testing via curl:
  ```bash
  curl http://localhost:8001/api/prices
  curl http://localhost:8001/api/portfolio
  ```
- Browser testing: Tüm sayfalar manuel olarak test edildi
- Backend testing agent kullanıldı (`deep_testing_backend_v2`)
- Screenshot tool ile UI kontrol edildi

**Test Sonuçları:**
- ✅ API endpoint'leri çalışıyor
- ✅ Frontend-backend iletişimi sorunsuz
- ✅ Canlı fiyatlar doğru gösteriliyor
- ✅ Dönüştürücü hesaplamalar doğru
- ✅ Portföy CRUD operasyonları çalışıyor
- ✅ Dil değiştirme fonksiyonel

#### 10. Deployment Hazırlığı Planlaması
**Tartışılan Konular:**
- Backend deploy edilmeden önce mobil app build edilemez (localhost sorunu)
- Admin panel web-only olacak (mobil app içinde değil)
- Capacitor ile native iOS/Android build yapılacak
- Splash screen ve app icon gerekli
- Google Play Store ve Apple App Store submission süreci

**Kullanıcı ile Anlaşılan Plan:**
1. Backend deployment
2. Admin panel geliştirme ve deployment
3. Final web app testing
4. Kar marjı bilgilerini alma
5. Gerekli değişiklikleri yapma
6. Capacitor build
7. App Store submission

---

## BUNDAN SONRA YAPILACAKLAR

### FAZ 1: ADMIN PANEL & BACKEND DEPLOYMENT
**Tahmini Süre**: ~100 kredi
**Öncelik**: P0 (En Yüksek)

---

#### GÖREV 1.1: MongoDB Admin Collections Oluşturma
**Dosya**: `backend/server.py`, `backend/models.py`

**Adımlar:**

**1.1.1: Pydantic Models Oluştur**
```python
# models.py içine ekle

from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str
    hashed_password: str
    created_at: str
    is_active: bool = True

class UserLogin(BaseModel):
    username: str
    password: str

class Margin(BaseModel):
    product_id: int
    product_name: str
    product_name_en: str
    margin_percentage: float
    category: str  # "gold" veya "currency"
    updated_at: str
    updated_by: str  # admin username

class MarginUpdate(BaseModel):
    margin_percentage: float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
```

**1.1.2: MongoDB Collections Hazırla**
- Collection names:
  - `users` - Admin kullanıcı bilgileri
  - `margins` - Ürün bazlı kar marjları

**1.1.3: İlk Admin Kullanıcısını Manuel Olarak Ekle**
```python
# Tek seferlik script (backend/create_admin.py)
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    MONGO_URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("DB_NAME")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Kullanıcıdan input al (VEYA kullanıcının verdiği bilgileri kullan)
    username = input("Admin username: ")
    password = input("Admin password: ")
    
    hashed_pw = pwd_context.hash(password)
    
    admin_user = {
        "username": username,
        "hashed_password": hashed_pw,
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    result = await db.users.insert_one(admin_user)
    print(f"Admin created with ID: {result.inserted_id}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
```

**Çalıştırma:**
```bash
cd /app/backend
python create_admin.py
# Username ve password gir
```

---

#### GÖREV 1.2: JWT Authentication Sistemi Kurulumu
**Dosya**: `backend/auth.py` (yeni), `backend/server.py`

**Adımlar:**

**1.2.1: Gerekli Paketleri Kur**
```bash
cd /app/backend
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
pip freeze > requirements.txt
```

**1.2.2: auth.py Dosyası Oluştur**
```python
# backend/auth.py

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# JWT Settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 saat

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_current_user(token: str = Depends(oauth2_scheme), db=None):
    username = verify_token(token)
    user = await db.users.find_one({"username": username}, {"_id": 0})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
```

**1.2.3: JWT_SECRET_KEY'i .env'e Ekle**
```bash
# backend/.env'e ekle
JWT_SECRET_KEY=berkay-altin-super-secret-key-2025-change-in-production
```

---

#### GÖREV 1.3: Admin API Endpoint'leri Oluşturma
**Dosya**: `backend/server.py`

**Adımlar:**

**1.3.1: Admin Login Endpoint**
```python
# server.py'ye ekle

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import (
    verify_password, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import Token, UserLogin
from datetime import timedelta

@app.post("/api/admin/login", response_model=Token)
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Kullanıcıyı bul
    user = await db.users.find_one({"username": form_data.username}, {"_id": 0})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Şifreyi doğrula
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Kullanıcı aktif mi?
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )
    
    # JWT token oluştur
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

**1.3.2: Get Current User Endpoint (Test için)**
```python
@app.get("/api/admin/me")
async def get_admin_me(current_user = Depends(lambda: get_current_user(db=db))):
    return {
        "username": current_user["username"],
        "created_at": current_user["created_at"]
    }
```

**1.3.3: Get All Margins Endpoint**
```python
@app.get("/api/admin/margins")
async def get_all_margins(current_user = Depends(lambda: get_current_user(db=db))):
    # Mevcut fiyatları al
    prices = await get_harem_prices()
    
    # Tüm margin'leri al
    margins_data = await db.margins.find({}, {"_id": 0}).to_list(1000)
    
    # Margin dictionary oluştur (product_id -> margin_percentage)
    margins_dict = {m["product_id"]: m["margin_percentage"] for m in margins_data}
    
    # Gold ve currency listelerini margin bilgisi ile birleştir
    gold_with_margins = []
    for item in prices["gold"]:
        margin = margins_dict.get(item["id"], 0.0)
        gold_with_margins.append({
            **item,
            "margin_percentage": margin,
            "category": "gold"
        })
    
    currency_with_margins = []
    for item in prices["currency"]:
        margin = margins_dict.get(item["id"], 0.0)
        currency_with_margins.append({
            **item,
            "margin_percentage": margin,
            "category": "currency"
        })
    
    return {
        "gold": gold_with_margins,
        "currency": currency_with_margins
    }
```

**1.3.4: Update Margin Endpoint**
```python
from models import MarginUpdate
from datetime import datetime

@app.put("/api/admin/margins/{product_id}")
async def update_margin(
    product_id: int,
    margin_data: MarginUpdate,
    current_user = Depends(lambda: get_current_user(db=db))
):
    # Önce ürünün mevcut olup olmadığını kontrol et
    prices = await get_harem_prices()
    all_products = prices["gold"] + prices["currency"]
    product = next((p for p in all_products if p["id"] == product_id), None)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Category belirle
    category = "gold" if product in prices["gold"] else "currency"
    
    # Margin'i güncelle veya oluştur
    margin_doc = {
        "product_id": product_id,
        "product_name": product["name"],
        "product_name_en": product["nameEn"],
        "margin_percentage": margin_data.margin_percentage,
        "category": category,
        "updated_at": datetime.now().isoformat(),
        "updated_by": current_user["username"]
    }
    
    # Upsert (update or insert)
    await db.margins.update_one(
        {"product_id": product_id},
        {"$set": margin_doc},
        upsert=True
    )
    
    return {"message": "Margin updated successfully", "margin": margin_doc}
```

**1.3.5: Bulk Update Margins Endpoint (Opsiyonel)**
```python
from typing import List
from pydantic import BaseModel

class BulkMarginUpdate(BaseModel):
    product_id: int
    margin_percentage: float

@app.post("/api/admin/margins/bulk-update")
async def bulk_update_margins(
    updates: List[BulkMarginUpdate],
    current_user = Depends(lambda: get_current_user(db=db))
):
    prices = await get_harem_prices()
    all_products = prices["gold"] + prices["currency"]
    
    updated_count = 0
    errors = []
    
    for update in updates:
        try:
            product = next((p for p in all_products if p["id"] == update.product_id), None)
            if not product:
                errors.append(f"Product {update.product_id} not found")
                continue
            
            category = "gold" if product in prices["gold"] else "currency"
            
            margin_doc = {
                "product_id": update.product_id,
                "product_name": product["name"],
                "product_name_en": product["nameEn"],
                "margin_percentage": update.margin_percentage,
                "category": category,
                "updated_at": datetime.now().isoformat(),
                "updated_by": current_user["username"]
            }
            
            await db.margins.update_one(
                {"product_id": update.product_id},
                {"$set": margin_doc},
                upsert=True
            )
            updated_count += 1
        except Exception as e:
            errors.append(f"Error updating product {update.product_id}: {str(e)}")
    
    return {
        "updated_count": updated_count,
        "errors": errors
    }
```

---

#### GÖREV 1.4: Fiyatları Margin ile Hesaplama
**Dosya**: `backend/harem_api_service.py`, `backend/server.py`

**Adımlar:**

**1.4.1: Margin Uygulama Fonksiyonu Ekle**
```python
# harem_api_service.py içine ekle

async def apply_margins(prices, db):
    """
    Fiyatlara kar marjlarını uygula
    """
    # Tüm margin'leri al
    margins_data = await db.margins.find({}, {"_id": 0}).to_list(1000)
    margins_dict = {m["product_id"]: m["margin_percentage"] for m in margins_data}
    
    # Gold prices'a margin uygula
    for item in prices["gold"]:
        margin = margins_dict.get(item["id"], 0.0)
        if margin > 0:
            item["buy"] = round(item["buy"] * (1 + margin / 100), 2)
            item["sell"] = round(item["sell"] * (1 + margin / 100), 2)
    
    # Currency prices'a margin uygula
    for item in prices["currency"]:
        margin = margins_dict.get(item["id"], 0.0)
        if margin > 0:
            item["buy"] = round(item["buy"] * (1 + margin / 100), 2)
            item["sell"] = round(item["sell"] * (1 + margin / 100), 2)
    
    return prices
```

**1.4.2: /api/prices Endpoint'ini Güncelle**
```python
# server.py'de güncelle

@app.get("/api/prices")
async def get_prices():
    try:
        # Önce raw fiyatları al
        prices = await get_harem_prices()
        
        # Margin'leri uygula
        from harem_api_service import apply_margins
        prices_with_margins = await apply_margins(prices, db)
        
        return prices_with_margins
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

#### GÖREV 1.5: Admin Panel Frontend Geliştirme
**Dosya**: `frontend/src/components/AdminPanel.js`, `frontend/src/App.js`

**Adımlar:**

**1.5.1: Admin Login Page Oluştur**
```javascript
// frontend/src/components/AdminLogin.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';

export default function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/login`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData
        }
      );

      if (!response.ok) {
        throw new Error('Giriş başarısız');
      }

      const data = await response.json();
      
      // Token'ı localStorage'a kaydet
      localStorage.setItem('admin_token', data.access_token);
      
      // Admin panele yönlendir
      navigate('/admin/dashboard');
    } catch (err) {
      setError('Kullanıcı adı veya şifre hatalı');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-2xl font-bold text-center mb-6">
          BERKAY ALTIN Admin
        </h1>
        
        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">
              Kullanıcı Adı
            </label>
            <Input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">
              Şifre
            </label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <Button 
            type="submit" 
            className="w-full"
            disabled={loading}
          >
            {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
          </Button>
        </form>
      </Card>
    </div>
  );
}
```

**1.5.2: Protected Route Component Oluştur**
```javascript
// frontend/src/components/ProtectedRoute.js

import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem('admin_token');
  
  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }
  
  return children;
}
```

**1.5.3: Admin Dashboard Oluştur**
```javascript
// frontend/src/components/AdminDashboard.js

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

export default function AdminDashboard() {
  const [margins, setMargins] = useState({ gold: [], currency: [] });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [tempMargin, setTempMargin] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchMargins();
  }, []);

  const fetchMargins = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/margins`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      if (response.status === 401) {
        // Token geçersiz, login'e yönlendir
        localStorage.removeItem('admin_token');
        navigate('/admin/login');
        return;
      }

      const data = await response.json();
      setMargins(data);
    } catch (error) {
      console.error('Margin verileri alınamadı:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (product) => {
    setEditingId(product.id);
    setTempMargin(product.margin_percentage.toString());
  };

  const handleSave = async (productId) => {
    setSaving(true);
    try {
      const token = localStorage.getItem('admin_token');
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/admin/margins/${productId}`,
        {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            margin_percentage: parseFloat(tempMargin)
          })
        }
      );

      if (response.ok) {
        setEditingId(null);
        fetchMargins(); // Refresh data
      }
    } catch (error) {
      console.error('Margin güncellenemedi:', error);
      alert('Güncelleme başarısız!');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setEditingId(null);
    setTempMargin('');
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    navigate('/admin/login');
  };

  const renderProductRow = (product, category) => {
    const isEditing = editingId === product.id;

    return (
      <tr key={product.id} className="border-b">
        <td className="py-3 px-4">{product.name}</td>
        <td className="py-3 px-4">{product.buy.toFixed(2)} TRY</td>
        <td className="py-3 px-4">{product.sell.toFixed(2)} TRY</td>
        <td className="py-3 px-4">
          {isEditing ? (
            <Input
              type="number"
              step="0.01"
              value={tempMargin}
              onChange={(e) => setTempMargin(e.target.value)}
              className="w-24"
            />
          ) : (
            <span>{product.margin_percentage}%</span>
          )}
        </td>
        <td className="py-3 px-4">
          {isEditing ? (
            <div className="flex gap-2">
              <Button 
                size="sm" 
                onClick={() => handleSave(product.id)}
                disabled={saving}
              >
                Kaydet
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                onClick={handleCancel}
                disabled={saving}
              >
                İptal
              </Button>
            </div>
          ) : (
            <Button 
              size="sm" 
              variant="outline" 
              onClick={() => handleEdit(product)}
            >
              Düzenle
            </Button>
          )}
        </td>
      </tr>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Yükleniyor...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Kar Marjı Yönetimi</h1>
          <Button variant="outline" onClick={handleLogout}>
            Çıkış Yap
          </Button>
        </div>

        <Card className="p-6">
          <Tabs defaultValue="gold">
            <TabsList className="mb-4">
              <TabsTrigger value="gold">Altın ({margins.gold.length})</TabsTrigger>
              <TabsTrigger value="currency">Döviz ({margins.currency.length})</TabsTrigger>
            </TabsList>

            <TabsContent value="gold">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2">
                      <th className="text-left py-3 px-4">Ürün</th>
                      <th className="text-left py-3 px-4">Alış</th>
                      <th className="text-left py-3 px-4">Satış</th>
                      <th className="text-left py-3 px-4">Kar Marjı</th>
                      <th className="text-left py-3 px-4">İşlem</th>
                    </tr>
                  </thead>
                  <tbody>
                    {margins.gold.map(product => renderProductRow(product, 'gold'))}
                  </tbody>
                </table>
              </div>
            </TabsContent>

            <TabsContent value="currency">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2">
                      <th className="text-left py-3 px-4">Ürün</th>
                      <th className="text-left py-3 px-4">Alış</th>
                      <th className="text-left py-3 px-4">Satış</th>
                      <th className="text-left py-3 px-4">Kar Marjı</th>
                      <th className="text-left py-3 px-4">İşlem</th>
                    </tr>
                  </thead>
                  <tbody>
                    {margins.currency.map(product => renderProductRow(product, 'currency'))}
                  </tbody>
                </table>
              </div>
            </TabsContent>
          </Tabs>
        </Card>

        <div className="mt-4 text-sm text-gray-600">
          <p>
            * Kar marjı oranları hem alış hem de satış fiyatlarına uygulanır.
          </p>
          <p>
            * Değişiklikler anında kullanıcı uygulamasına yansır.
          </p>
        </div>
      </div>
    </div>
  );
}
```

**1.5.4: Routes'u Güncelle (App.js)**
```javascript
// frontend/src/App.js

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ConverterPage from './components/ConverterPage';
import PortfolioPage from './components/PortfolioPage';
import AdminLogin from './components/AdminLogin';
import AdminDashboard from './components/AdminDashboard';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/converter" element={<ConverterPage />} />
        <Route path="/portfolio" element={<PortfolioPage />} />
        
        {/* Admin routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route 
          path="/admin/dashboard" 
          element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
```

---

#### GÖREV 1.6: Backend Deployment
**Platform Seçimi**: Heroku / Railway / DigitalOcean / AWS

**Adımlar:**

**1.6.1: Deployment için Hazırlık**

**Procfile Oluştur (Heroku için):**
```
web: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
```

**requirements.txt'i Kontrol Et:**
```bash
cd /app/backend
pip freeze > requirements.txt
```

**runtime.txt Oluştur (Python version):**
```
python-3.11.5
```

**1.6.2: MongoDB Atlas Kurulumu**
1. https://www.mongodb.com/atlas adresine git
2. Ücretsiz cluster oluştur (M0 Free Tier)
3. Database user oluştur (username & password)
4. Network Access'te IP whitelist'e `0.0.0.0/0` ekle (production'da spesifik IP olmalı)
5. Connection string'i kopyala:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

**1.6.3: Environment Variables (Production)**
```bash
# Deployment platformunda ayarlanacak env vars:
MONGO_URL=mongodb+srv://berkayaltin:XXXXXXXX@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=berkay_altin_production
RAPIDAPI_KEY=1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4
RAPIDAPI_HOST=harem-altin-live-gold-price-data.p.rapidapi.com
JWT_SECRET_KEY=super-secret-production-key-change-this
```

**1.6.4: Heroku Deployment (Örnek)**
```bash
# Heroku CLI kur
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Yeni app oluştur
heroku create berkay-altin-backend

# Environment variables ayarla
heroku config:set MONGO_URL="mongodb+srv://..."
heroku config:set DB_NAME="berkay_altin_production"
heroku config:set RAPIDAPI_KEY="1f83e11378..."
heroku config:set RAPIDAPI_HOST="harem-altin-live-gold-price-data.p.rapidapi.com"
heroku config:set JWT_SECRET_KEY="super-secret-production-key"

# Git push
git subtree push --prefix backend heroku main

# Logs kontrol
heroku logs --tail
```

**Deployed Backend URL:**
```
https://berkay-altin-backend.herokuapp.com
```

**Test Et:**
```bash
curl https://berkay-altin-backend.herokuapp.com/api/prices
```

---

#### GÖREV 1.7: Frontend Environment Update
**Dosya**: `frontend/.env`

**Adımlar:**

**1.7.1: .env'i Güncelle**
```bash
# frontend/.env
REACT_APP_BACKEND_URL=https://berkay-altin-backend.herokuapp.com
```

**1.7.2: Test Et (Local)**
```bash
cd /app/frontend
yarn start

# Browser'da aç: http://localhost:3000
# Prices yükleniyor mu kontrol et
```

---

#### GÖREV 1.8: Admin Panel Deployment
**Platform**: Vercel / Netlify (Önerilen)

**Adımlar:**

**1.8.1: Build Script Hazırla**
```bash
cd /app/frontend
yarn build
```

**1.8.2: Vercel Deployment (Örnek)**
```bash
# Vercel CLI kur
npm install -g vercel

# Login
vercel login

# Deploy
cd /app/frontend
vercel --prod

# Custom domain ayarla (opsiyonel)
# berkayaltin.com veya admin.berkayaltin.com
```

**Deployed Frontend URL:**
```
https://berkay-altin.vercel.app
```

**Admin Panel URL:**
```
https://berkay-altin.vercel.app/admin/login
```

---

#### GÖREV 1.9: Initial Admin User & Margins Setup
**Adımlar:**

**1.9.1: Production MongoDB'ye Admin Ekle**
```python
# Local'de script çalıştır, production MongoDB'ye bağlan

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    # PRODUCTION MONGO_URL kullan!
    MONGO_URL = "mongodb+srv://berkayaltin:XXXXX@cluster0.xxxxx.mongodb.net/"
    DB_NAME = "berkay_altin_production"
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # KULLANICIDAN ALINAN BİLGİLER
    username = "admin_berkay"  # Kullanıcının verdiği
    password = "güvenli-şifre-123"  # Kullanıcının verdiği
    
    hashed_pw = pwd_context.hash(password)
    
    admin_user = {
        "username": username,
        "hashed_password": hashed_pw,
        "created_at": datetime.now().isoformat(),
        "is_active": True
    }
    
    result = await db.users.insert_one(admin_user)
    print(f"✅ Admin created: {username}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
```

**1.9.2: Default Margin Değerlerini Ekle (Opsiyonel)**
```python
# Kullanıcıdan alınan margin değerlerini MongoDB'ye ekle

async def seed_margins():
    MONGO_URL = "mongodb+srv://..."
    DB_NAME = "berkay_altin_production"
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # KULLANICIDAN ALINAN MARGIN DEĞERLERİ
    default_margins = [
        {"product_id": 1, "category": "gold", "margin_percentage": 2.5},
        {"product_id": 2, "category": "gold", "margin_percentage": 2.5},
        # ... tüm ürünler için
    ]
    
    for margin in default_margins:
        await db.margins.insert_one(margin)
    
    print(f"✅ {len(default_margins)} margin seeded")
    client.close()
```

---

#### GÖREV 1.10: Testing (Backend + Admin Panel)
**Test Senaryoları:**

**1.10.1: Backend API Testing**
```bash
# 1. Health check (genel endpoint)
curl https://berkay-altin-backend.herokuapp.com/api/prices

# 2. Admin login
curl -X POST https://berkay-altin-backend.herokuapp.com/api/admin/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin_berkay&password=güvenli-şifre-123"

# Response: {"access_token": "eyJ...", "token_type": "bearer"}

# 3. Get margins (authenticated)
curl https://berkay-altin-backend.herokuapp.com/api/admin/margins \
  -H "Authorization: Bearer eyJ..."

# 4. Update margin
curl -X PUT https://berkay-altin-backend.herokuapp.com/api/admin/margins/1 \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"margin_percentage": 3.5}'
```

**1.10.2: Admin Panel UI Testing**
- https://berkay-altin.vercel.app/admin/login adresine git
- Kullanıcı adı ve şifre ile giriş yap
- Dashboard'da tüm ürünleri görüntüle
- Bir ürünün margin'ini düzenle ve kaydet
- Logout yap ve tekrar giriş yap (session kontrolü)

**1.10.3: Integration Testing**
- Web app'te (https://berkay-altin.vercel.app) fiyatları görüntüle
- Admin panel'de bir margin değiştir
- Web app'i yenile, fiyatların güncellendiğini doğrula

**1.10.4: Testing Agent Kullanımı**
```
deep_testing_backend_v2(
  "Test the deployed backend API and admin authentication flow:
  1. Test /api/prices endpoint for live data
  2. Test admin login with correct and incorrect credentials
  3. Test JWT token validation
  4. Test margin CRUD operations
  5. Test that prices reflect margin changes
  6. Test unauthorized access attempts
  
  Backend URL: https://berkay-altin-backend.herokuapp.com
  Admin credentials: [provide]"
)
```

---

### FAZ 2: CAPACITOR BUILD & MOBILE APP
**Tahmini Süre**: ~60 kredi
**Öncelik**: P3

---

#### GÖREV 2.1: Final Web App Testing
**Dosya**: Tüm frontend components

**Adımlar:**

**2.1.1: Functional Testing**
- Ana sayfa: Fiyatlar yükleniyor mu?
- Dönüştürücü: Hesaplamalar doğru mu?
- Portföy: CRUD operasyonları çalışıyor mu?
- Dil değiştirme: TR/EN geçişi sorunsuz mu?
- Admin panel: Login, margin update, logout çalışıyor mu?

**2.1.2: UI/UX Testing**
- Mobil görünüm (375px): Layout bozuk mu?
- Butonlar tıklanabilir mi?
- Form validasyonları var mı?
- Loading states gösteriliyor mu?
- Error messages kullanıcı dostu mu?

**2.1.3: Performance Testing**
- Sayfa yükleme süreleri
- API response süreleri
- Image optimization
- Bundle size

**2.1.4: Cross-browser Testing**
- Chrome (Android)
- Safari (iOS)
- Firefox
- Edge

**2.1.5: Testing Agent Kullanımı**
```
auto_frontend_testing_agent(
  "Comprehensive E2E testing of BERKAY ALTIN app:
  
  Test Flow 1: Public User Journey
  1. Open homepage, verify prices load
  2. Switch between gold and currency tabs
  3. Change language TR/EN
  4. Navigate to converter
  5. Select products and convert
  6. Navigate to portfolio
  7. Add a portfolio item
  8. Delete a portfolio item
  
  Test Flow 2: Admin Journey
  9. Navigate to /admin/login
  10. Attempt login with wrong credentials (should fail)
  11. Login with correct credentials
  12. Verify dashboard loads with all products
  13. Edit a margin value and save
  14. Verify success message
  15. Logout
  
  Test Flow 3: Price Update Verification
  16. Admin changes margin for 'Gram Altın' to 5%
  17. Public user refreshes homepage
  18. Verify 'Gram Altın' price increased by 5%
  
  App URL: https://berkay-altin.vercel.app
  Admin URL: https://berkay-altin.vercel.app/admin/login
  Credentials: [provide]
  
  Expected behavior: All flows should complete without errors
  Screenshot critical steps"
)
```

---

#### GÖREV 2.2: Logo & Splash Screen Hazırlığı
**Gerekli Dosyalar:**
- App Icon (1024x1024 PNG)
- Splash Screen (2732x2732 PNG)

**Adımlar:**

**2.2.1: Logo Tasarımı (Kullanıcıdan İstenecek VEYA Önerilecek)**

**Öneriler:**
- **Tema**: Altın rengi (#FFD700), modern, minimal
- **İçerik**: "BERKAY ALTIN" text + altın çubuğu ikonu
- **Format**: PNG, şeffaf arka plan
- **Boyut**: 1024x1024 px

**2.2.2: Splash Screen Tasarımı**

**Öneriler:**
- **Arka Plan**: Koyu yeşil gradient (#1e3a2f → #2d5a3d)
- **Orta**: Logo (512x512)
- **Alt**: "BERKAY ALTIN" text (beyaz, 48pt)
- **Format**: PNG
- **Boyut**: 2732x2732 px

**2.2.3: Asset Generator Kullanımı**

**Capacitor Asset Generator:**
```bash
npm install -g @capacitor/assets

# Assets klasörü oluştur
mkdir /app/frontend/assets

# Logo ve splash screen'i koy:
# /app/frontend/assets/icon.png (1024x1024)
# /app/frontend/assets/splash.png (2732x2732)

# Tüm boyutları otomatik oluştur
cd /app/frontend
npx @capacitor/assets generate --iconPath assets/icon.png --splashPath assets/splash.png
```

Bu komut otomatik olarak:
- iOS için tüm icon boyutlarını (AppIcon)
- Android için tüm icon boyutlarını (mipmap)
- iOS için tüm splash boyutlarını (LaunchScreen)
- Android için tüm splash boyutlarını (drawable)
oluşturur.

---

#### GÖREV 2.3: Capacitor Kurulumu
**Dosya**: `frontend/` directory

**Adımlar:**

**2.3.1: Capacitor CLI ve Core Paketleri Kur**
```bash
cd /app/frontend

# Core packages
yarn add @capacitor/core @capacitor/cli

# Platform packages
yarn add @capacitor/android @capacitor/ios

# Ek plugin'ler
yarn add @capacitor/splash-screen @capacitor/status-bar @capacitor/app
```

**2.3.2: Capacitor'ı İnisiyalize Et**
```bash
npx cap init "BERKAY ALTIN" "com.berkayaltin.app" --web-dir=build
```

Bu komut:
- `capacitor.config.json` dosyası oluşturur
- App name: "BERKAY ALTIN"
- App ID: "com.berkayaltin.app" (Android package name)
- Web directory: "build" (React build output)

**2.3.3: capacitor.config.json Düzenle**
```json
{
  "appId": "com.berkayaltin.app",
  "appName": "BERKAY ALTIN",
  "webDir": "build",
  "bundledWebRuntime": false,
  "server": {
    "androidScheme": "https"
  },
  "plugins": {
    "SplashScreen": {
      "launchShowDuration": 2000,
      "launchAutoHide": true,
      "backgroundColor": "#1e3a2f",
      "androidSplashResourceName": "splash",
      "androidScaleType": "CENTER_CROP",
      "showSpinner": false
    },
    "StatusBar": {
      "style": "LIGHT",
      "backgroundColor": "#1e3a2f"
    }
  }
}
```

**2.3.4: Environment Variables için Capacitor Config Ekle**
```javascript
// capacitor.config.ts (veya .json yerine .ts kullan)

import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.berkayaltin.app',
  appName: 'BERKAY ALTIN',
  webDir: 'build',
  bundledWebRuntime: false,
  server: {
    androidScheme: 'https',
    // Production backend URL
    url: 'https://berkay-altin.vercel.app', // VEYA ayrı bir mobile build
    cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: true,
      backgroundColor: '#1e3a2f',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false
    },
    StatusBar: {
      style: 'LIGHT',
      backgroundColor: '#1e3a2f'
    }
  }
};

export default config;
```

---

#### GÖREV 2.4: Android Platform Ekleme
**Adımlar:**

**2.4.1: React App'i Build Et**
```bash
cd /app/frontend
yarn build
```

**2.4.2: Android Platform Ekle**
```bash
npx cap add android
```

Bu komut:
- `android/` klasörü oluşturur
- Gradle build files'ları hazırlar
- AndroidManifest.xml oluşturur
- Build'lenmiş React app'i android/app/src/main/assets/public/ klasörüne kopyalar

**2.4.3: Web Assets'i Android'e Sync Et**
```bash
npx cap sync android
```

**2.4.4: Android Studio'da Aç (Opsiyonel, Debug için)**
```bash
npx cap open android
```

---

#### GÖREV 2.5: iOS Platform Ekleme (macOS gerekli)
**NOT**: iOS build için macOS + Xcode gereklidir. Eğer macOS yoksa, bu adım kullanıcı tarafından yapılmalı.

**Adımlar:**

**2.5.1: iOS Platform Ekle**
```bash
cd /app/frontend
npx cap add ios
```

**2.5.2: Web Assets'i iOS'e Sync Et**
```bash
npx cap sync ios
```

**2.5.3: Xcode'da Aç**
```bash
npx cap open ios
```

**2.5.4: Xcode'da Gerekli Ayarlar**
- Signing & Capabilities: Development team seç
- Bundle Identifier: com.berkayaltin.app
- Deployment Target: iOS 13.0 veya üzeri
- Icon & Splash Screen: Otomatik eklenir (asset generator sayesinde)

---

#### GÖREV 2.6: APK/AAB Build (Android)
**Adımlar:**

**2.6.1: Android Studio'da Build**

**Debug APK (Test için):**
```bash
cd /app/frontend/android
./gradlew assembleDebug

# Output: android/app/build/outputs/apk/debug/app-debug.apk
```

**Release APK (Dağıtım için):**

**Keystore Oluştur:**
```bash
keytool -genkey -v -keystore berkay-altin-release.keystore -alias berkay-altin -keyalg RSA -keysize 2048 -validity 10000

# Sorular:
# - Password: güvenli-şifre-123
# - Name: Berkay
# - Organization: BERKAY ALTIN
# - vb.
```

**android/app/build.gradle Düzenle:**
```gradle
android {
    ...
    
    signingConfigs {
        release {
            storeFile file("../../berkay-altin-release.keystore")
            storePassword "güvenli-şifre-123"
            keyAlias "berkay-altin"
            keyPassword "güvenli-şifre-123"
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

**Release APK Build:**
```bash
cd /app/frontend/android
./gradlew assembleRelease

# Output: android/app/build/outputs/apk/release/app-release.apk
```

**Release AAB Build (Google Play Store için):**
```bash
cd /app/frontend/android
./gradlew bundleRelease

# Output: android/app/build/outputs/bundle/release/app-release.aab
```

**2.6.2: APK Test Et**
```bash
# Android emulator veya gerçek cihazda
adb install android/app/build/outputs/apk/debug/app-debug.apk

# Uygulamayı aç ve test et
```

---

#### GÖREV 2.7: App Store Assets Hazırlığı
**Gerekli Materyaller:**

**Google Play Store:**
1. **App Icon**: 512x512 PNG (Hi-res icon)
2. **Feature Graphic**: 1024x500 PNG
3. **Screenshots**: 
   - Phone: En az 2 screenshot (max 8)
   - 7-inch tablet: Opsiyonel
   - 10-inch tablet: Opsiyonel
   - Önerilen boyut: 1080x1920 (portrait)
4. **Short Description**: Max 80 karakter
5. **Full Description**: Max 4000 karakter
6. **App Category**: Finance
7. **Privacy Policy URL**: Gerekli
8. **Contact Email**: Gerekli

**Apple App Store:**
1. **App Icon**: 1024x1024 PNG (App Store icon)
2. **Screenshots**: 
   - 6.5" Display (iPhone 14 Pro Max): 1290x2796
   - 5.5" Display (iPhone 8 Plus): 1242x2208
   - iPad Pro 12.9": 2048x2732
   - En az 1 screenshot her ekran boyutu için
3. **App Preview Video**: Opsiyonel
4. **Description**: Max 4000 karakter
5. **Keywords**: Max 100 karakter
6. **Support URL**: Gerekli
7. **Privacy Policy URL**: Gerekli

**2.7.1: Screenshot'ları Al**
- Testing agent ile Playwright kullanarak:
```
auto_frontend_testing_agent(
  "Take high-quality screenshots for app store submission:
  1. Homepage with live gold prices (Turkish)
  2. Currency tab with exchange rates
  3. Converter page with sample conversion
  4. Portfolio page with sample items
  5. Language switch to English
  6. Homepage in English
  
  Device: iPhone 14 Pro Max (1290x2796)
  Make sure prices are visible and UI looks clean
  No personal data in screenshots"
)
```

**2.7.2: Store Listing Texts Hazırla**

**Short Description (TR):**
```
Canlı altın ve döviz fiyatları, dönüştürücü ve portföy yönetimi.
```

**Short Description (EN):**
```
Live gold and currency prices, converter, and portfolio management.
```

**Full Description (TR):**
```
BERKAY ALTIN - Güncel Altın ve Döviz Fiyatları

📊 Canlı Fiyatlar
• Gram altın, çeyrek altın, tam altın ve daha fazlası
• USD, EUR, GBP ve 10+ döviz kuru
• Anlık piyasa verileri
• Günlük değişim oranları

🔄 Dönüştürücü
• Altın ve döviz birimlerini anında dönüştürün
• Hem alış hem de satış fiyatlarıyla hesaplama
• Kolay kullanımlı arayüz

💼 Portföy Yönetimi
• Altın ve döviz varlıklarınızı takip edin
• Toplam portföy değerinizi görün
• Kolayca ekleme ve silme

🌍 Çoklu Dil Desteği
• Türkçe
• English

✨ Özellikler
• Mobil optimize tasarım
• Hızlı ve güvenilir
• Reklamsız deneyim
• Ücretsiz kullanım

BERKAY ALTIN ile altın ve döviz piyasasını takip etmek artık çok kolay!
```

**Full Description (EN):**
```
BERKAY ALTIN - Live Gold and Currency Prices

📊 Live Prices
• Gram gold, quarter gold, full gold and more
• USD, EUR, GBP and 10+ currency rates
• Real-time market data
• Daily change percentages

🔄 Converter
• Instantly convert gold and currency units
• Calculate with both buy and sell prices
• Easy-to-use interface

💼 Portfolio Management
• Track your gold and currency assets
• See your total portfolio value
• Easy add and delete

🌍 Multi-Language Support
• Turkish (Türkçe)
• English

✨ Features
• Mobile-optimized design
• Fast and reliable
• Ad-free experience
• Free to use

Stay updated with the gold and currency market with BERKAY ALTIN!
```

---

#### GÖREV 2.8: Privacy Policy Oluşturma
**Gereklilik**: Her iki app store da privacy policy gerektirir.

**Adımlar:**

**2.8.1: Privacy Policy Generator Kullan**
- https://www.privacypolicygenerator.info/ (ücretsiz)
- Veya ChatGPT ile özel policy oluştur

**2.8.2: Policy İçeriği (Örnek)**
```markdown
# Privacy Policy for BERKAY ALTIN

Last updated: [DATE]

## Information We Collect
BERKAY ALTIN does not collect, store, or share any personal information.

## Data Usage
- All market data is fetched from public APIs
- Portfolio data is stored locally on your device
- No user accounts or login required for the main app
- Admin panel uses secure authentication but is not accessible to public users

## Third-Party Services
We use the following third-party services:
- RapidAPI (Harem Altın Live Gold Price Data): For fetching live market prices

## Changes to This Policy
We may update this policy from time to time. Any changes will be posted on this page.

## Contact Us
If you have any questions about this privacy policy, please contact us at:
[EMAIL]
```

**2.8.3: Policy'yi Hosting**
- GitHub Pages (ücretsiz)
- Vercel (zaten frontend hosted ise, /privacy route'u ekle)

**Frontend'de Privacy Route Ekle:**
```javascript
// frontend/src/components/PrivacyPolicy.js

export default function PrivacyPolicy() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
      {/* Policy content */}
    </div>
  );
}

// App.js'e route ekle
<Route path="/privacy" element={<PrivacyPolicy />} />
```

**URL**: https://berkay-altin.vercel.app/privacy

---

#### GÖREV 2.9: Google Play Store Submission
**Gereksinimler:**
- Google Play Developer hesabı ($25 one-time fee)
- app-release.aab dosyası
- Tüm store assets

**Adımlar:**

**2.9.1: Google Play Console'a Giriş**
- https://play.google.com/console
- "Create App" butonuna tıkla

**2.9.2: App Bilgilerini Doldur**
- App name: BERKAY ALTIN
- Default language: Turkish
- App or game: App
- Free or paid: Free
- Category: Finance
- Privacy policy: https://berkay-altin.vercel.app/privacy
- Contact email: [kullanıcının emaili]

**2.9.3: Store Listing**
- Upload icon (512x512)
- Upload feature graphic (1024x500)
- Upload screenshots (en az 2)
- Short description
- Full description

**2.9.4: App Release - Production**
- Countries/regions: Turkey (veya global)
- Create new release
- Upload app-release.aab
- Release name: 1.0.0
- Release notes:
  ```
  İlk sürüm:
  - Canlı altın ve döviz fiyatları
  - Dönüştürücü
  - Portföy yönetimi
  - TR/EN dil desteği
  ```

**2.9.5: Content Rating**
- Questionnaire doldur (Finance app, no violence, no ads)
- Rating: Everyone

**2.9.6: App Content**
- Privacy policy: ✅
- Ads: No
- Data safety: Fill form (no data collection)

**2.9.7: Review and Publish**
- "Send for review" butonuna tıkla
- Review süresi: 2-7 gün

---

#### GÖREV 2.10: Apple App Store Submission
**Gereksinimler:**
- Apple Developer Program ($99/year)
- macOS + Xcode
- Signed IPA file

**Adımlar:**

**2.10.1: App Store Connect'e Giriş**
- https://appstoreconnect.apple.com
- "My Apps" → "+" → "New App"

**2.10.2: App Bilgileri**
- Name: BERKAY ALTIN
- Primary language: Turkish
- Bundle ID: com.berkayaltin.app
- SKU: berkay-altin-001

**2.10.3: Pricing and Availability**
- Price: Free
- Availability: Turkey (veya global)

**2.10.4: App Information**
- Category: Finance
- Secondary category: Utilities (opsiyonel)
- Privacy policy URL: https://berkay-altin.vercel.app/privacy
- Support URL: https://berkay-altin.vercel.app/support (oluşturulmalı)

**2.10.5: Version Information (1.0)**
- Screenshots: Upload for all required sizes
- Description: [Full description EN]
- Keywords: gold, currency, exchange rate, price, portfolio, finance
- Promotional text: Track live gold and currency prices in Turkey

**2.10.6: Build Upload (Xcode)**
```bash
# Xcode'da:
# 1. Product → Archive
# 2. Archives window'da "Distribute App"
# 3. "App Store Connect" seç
# 4. Upload
# 5. Wait for processing (5-30 mins)
```

**2.10.7: App Review Information**
- Contact: [email & phone]
- Demo account: N/A (no login required for main features)
- Notes: "Admin panel at /admin/login is for internal use only"

**2.10.8: Submit for Review**
- Review süresi: 1-3 gün (genellikle 24-48 saat)

---

#### GÖREV 2.11: Post-Submission Testing
**Adımlar:**

**2.11.1: Internal Testing (TestFlight for iOS)**
- TestFlight invite linki oluştur
- Beta tester'lara gönder
- Feedback topla

**2.11.2: Closed Beta (Google Play)**
- Internal testing track oluştur
- Tester email listesi ekle
- Feedback topla

**2.11.3: Bug Fixes (Eğer varsa)**
- Testte bulunan bug'ları fix et
- Yeni build upload et
- Re-test

**2.11.4: Public Release**
- Google Play: "Publish to Production"
- Apple: "Release this version"

---

### FAZ 3: POST-LAUNCH & MAINTENANCE
**Sürekli**

---

#### GÖREV 3.1: Monitoring ve Analytics
**Adımlar:**

**3.1.1: Backend Monitoring**
- Heroku logs: `heroku logs --tail`
- Uptime monitoring: UptimeRobot (ücretsiz)
- Error tracking: Sentry (opsiyonel)

**3.1.2: App Analytics**
- Google Analytics for Firebase (ücretsiz)
- User engagement metrics
- Crash reporting

**3.1.3: API Usage Tracking**
- RapidAPI usage limits kontrol
- MongoDB Atlas usage (free tier: 512 MB)

---

#### GÖREV 3.2: Bug Fixing ve Updates
**Adımlar:**

**3.2.1: User Feedback Toplama**
- App Store reviews kontrol
- Play Store reviews kontrol
- Email feedback

**3.2.2: Bug Fix Process**
1. Bug'ı reproduce et
2. Fix'i implement et
3. Test et (local + staging)
4. Version bump: 1.0.0 → 1.0.1
5. Build new APK/AAB/IPA
6. Submit to stores

**3.2.3: Feature Updates**
- User requests değerlendir
- Priority'ye göre planlama
- Development cycle: Design → Implement → Test → Deploy

---

#### GÖREV 3.3: API Key Management
**Adımlar:**

**3.3.1: Key Rotation**
- RapidAPI key'i düzenli kontrol
- Expired key durumunda yeni key oluştur
- Backend .env'i güncelle
- Redeploy

**3.3.2: MongoDB Backup**
- MongoDB Atlas auto-backup aktif et
- Manuel snapshot al (kritik güncellemelerden önce)

---

#### GÖREV 3.4: Cost Management
**Aylık Maliyetler:**

**Development (One-time):**
- Emergent credits: ~160 kredi (tamamlandı)

**Hosting:**
- Backend (Heroku): $0-7/month (Hobby tier)
- MongoDB Atlas: $0 (free tier, 512 MB)
- Frontend (Vercel): $0 (free tier)

**Mobile:**
- Google Play: $25 (one-time)
- Apple Developer: $99/year

**Toplam Aylık**: ~$5-10 (ilk yıl $100 ekstra Apple için)

---

## TEKNİK DETAYLAR VE ÖZEL NOTLAR

### MongoDB Veritabanı Şeması

#### Collection: `portfolio_items`
```javascript
{
  "id": "550e8400-e29b-41d4-a716-446655440000", // UUID string
  "name": "Gram Altın",
  "amount": 10.5,
  "value": 60000.00,
  "type": "gold", // veya "currency" (opsiyonel)
  "created_at": "2025-12-01T10:30:00Z" // (opsiyonel)
}
```

#### Collection: `users` (Admin)
```javascript
{
  "username": "admin_berkay",
  "hashed_password": "$2b$12$...", // bcrypt hash
  "created_at": "2025-12-01T08:00:00Z",
  "is_active": true
}
```

#### Collection: `margins`
```javascript
{
  "product_id": 1,
  "product_name": "GRAM ALTIN",
  "product_name_en": "GRAM GOLD",
  "margin_percentage": 2.5,
  "category": "gold", // "gold" veya "currency"
  "updated_at": "2025-12-01T12:00:00Z",
  "updated_by": "admin_berkay"
}
```

### API Response Formats

#### GET /api/prices
```json
{
  "lastUpdate": "2025-12-01T22:28:31.489116",
  "gold": [
    {
      "id": 1,
      "name": "GRAM ALTIN",
      "nameEn": "GRAM GOLD",
      "buy": 5772.46,
      "sell": 5869.82,
      "change": 1.59,
      "unit": "TRY"
    }
  ],
  "currency": [
    {
      "id": 1,
      "name": "USD",
      "nameEn": "USD",
      "buy": 42.3,
      "sell": 42.72,
      "change": 1.21,
      "symbol": "$",
      "unit": "TRY"
    }
  ]
}
```

### Environment Variables Reference

#### Backend (.env)
```bash
# Database
MONGO_URL=mongodb://localhost:27017  # Local development
# MONGO_URL=mongodb+srv://...  # Production (MongoDB Atlas)
DB_NAME=berkay_altin_db

# RapidAPI
RAPIDAPI_KEY=1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4
RAPIDAPI_HOST=harem-altin-live-gold-price-data.p.rapidapi.com

# JWT (Production'da değiştirilmeli!)
JWT_SECRET_KEY=berkay-altin-super-secret-key-2025-change-in-production
```

#### Frontend (.env)
```bash
# Development (localhost backend)
# REACT_APP_BACKEND_URL=http://localhost:8001

# Production (deployed backend)
REACT_APP_BACKEND_URL=https://berkay-altin-backend.herokuapp.com
```

### Critical Commands Reference

#### Supervisor
```bash
# Status
sudo supervisorctl status

# Restart
sudo supervisorctl restart backend
sudo supervisorctl restart frontend

# Logs
tail -n 100 /var/log/supervisor/backend.err.log
tail -n 100 /var/log/supervisor/frontend.err.log
```

#### Package Management
```bash
# Backend (Python)
cd /app/backend
pip install <package>
pip freeze > requirements.txt
sudo supervisorctl restart backend

# Frontend (Yarn - NOT npm!)
cd /app/frontend
yarn add <package>
sudo supervisorctl restart frontend
```

#### Testing
```bash
# Backend API
curl http://localhost:8001/api/prices

# Frontend
curl http://localhost:3000

# Admin login
curl -X POST http://localhost:8001/api/admin/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=pass"
```

### Known Issues & Workarounds

#### Issue #1: MongoDB ObjectId Serialization
**Problem**: FastAPI can't serialize MongoDB `_id` field
**Solution**: Always exclude `_id` in queries:
```python
items = await db.collection.find({}, {"_id": 0}).to_list(1000)
```

#### Issue #2: CORS Errors
**Problem**: Frontend can't access backend API
**Solution**: Ensure CORS middleware is configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain olmalı
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Issue #3: Environment Variables Not Loading
**Problem**: `os.getenv()` returns `None`
**Solution**: Call `load_dotenv()` BEFORE any imports that use env vars:
```python
from dotenv import load_dotenv
load_dotenv()  # ÖNCE

from harem_api_service import get_harem_prices  # SONRA
```

### Security Best Practices

#### Production Checklist:
- [ ] JWT_SECRET_KEY değiştirildi (güçlü, random)
- [ ] MongoDB Atlas IP whitelist konfigüre edildi
- [ ] CORS origins spesifik domain'e daraltıldı
- [ ] Admin panel güçlü şifre kullanıyor
- [ ] HTTPS aktif (Let's Encrypt)
- [ ] API rate limiting implementasyonu (opsiyonel)
- [ ] Sensitive data log'lanmıyor

### Performance Optimization

#### Backend:
- MongoDB connection pooling (Motor default)
- Async/await kullanımı (FastAPI best practice)
- Response caching (opsiyonel, 30 saniye TTL)

#### Frontend:
- React.memo for expensive components
- Lazy loading for routes
- Image optimization (WebP format)
- Bundle size minimize (code splitting)

### Capacitor Specific Notes

#### Deep Links (Opsiyonel)
Eğer ileride web'den mobil app'e yönlendirme gerekirse:
```json
// capacitor.config.json
{
  "plugins": {
    "AppUrlOpen": {
      "url": "berkayaltin://",
      "androidScheme": "https",
      "iosSchemeName": "berkayaltin"
    }
  }
}
```

#### Push Notifications (Gelecek Feature)
```bash
yarn add @capacitor/push-notifications
```

---

## SONUÇ

Bu doküman, BERKAY ALTIN projesinin baştan sona tüm teknik detaylarını içermektedir. 

**Mevcut Durum**: ✅ Faz 0 (Core Development) tamamlandı
**Sonraki Adım**: 🔴 Faz 1 (Admin Panel & Deployment) başlamalı

**Kullanıcıdan Beklenen Bilgiler:**
1. Kar marjı yüzdeleri (her ürün için)
2. Admin panel kullanıcı adı ve şifresi
3. Logo/Splash screen tasarımı (opsiyonel, önerilebilir)

**Tahmini Toplam Süre**: ~160 kredi (Faz 1: 100 + Faz 2: 60)
**Deployment Sonrası Maliyet**: ~$10/month + $99/year (Apple)

---

**Son Güncelleme**: 2025-12-01
**Proje Durumu**: ✅ Development Complete | 🟡 Awaiting Deployment Info
**GitHub**: https://github.com/aberk4y/berkay-altin
