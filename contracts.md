# Harem Altın - API Contracts & Implementation Plan

## Backend API Endpoints

### 1. Gold & Currency Prices API
**Endpoint:** `GET /api/prices`
**Description:** Get real-time gold and currency prices from RapidAPI
**Query Parameters:**
- `type`: 'gold' | 'currency' | 'all' (default: 'all')

**Response:**
```json
{
  "gold": [
    {
      "id": 1,
      "name": "HAS ALTIN",
      "nameEn": "PURE GOLD",
      "buy": 5807.50,
      "sell": 5858.70,
      "change": 0.74,
      "unit": "TRY"
    }
  ],
  "currency": [
    {
      "id": 1,
      "name": "USD",
      "nameEn": "USD",
      "buy": 34.125,
      "sell": 34.225,
      "change": 0.55,
      "symbol": "$",
      "unit": "TRY"
    }
  ],
  "lastUpdate": "2024-12-01T18:35:00Z"
}
```

### 2. Portfolio Management

**Create Portfolio Item:** `POST /api/portfolio`
```json
{
  "type": "gold",
  "name": "GRAM ALTIN",
  "nameEn": "GRAM GOLD",
  "quantity": 50,
  "buyPrice": 5650.0
}
```

**Get Portfolio:** `GET /api/portfolio`
**Update Item:** `PUT /api/portfolio/{id}`
**Delete Item:** `DELETE /api/portfolio/{id}`

## RapidAPI Integration

**API Selected:** "Gold and Foreign Exchange Information from Turkish Companies"
- Endpoint: https://rapidapi.com/mu.butun/api/gold-and-foreign-exchange-information-from-turkish-companies
- API Key: 1f83e11378msh672d7bb8e29fb22p12e292jsn8d837cffc2b4

**Data Mapping:**
- HAS ALTIN (Has Altın)
- ONS (Ons)
- ÇEYREK ALTIN (Quarter Gold)
- YARIM ALTIN (Half Gold)
- TAM ALTIN (Full Gold)
- 22 AYAR (22 Carat)
- GRAM ALTIN (Gram Gold)
- USD, EUR, GBP, CHF, etc.

## MongoDB Collections

### Portfolio Collection
```json
{
  "_id": ObjectId,
  "userId": "default",
  "type": "gold" | "currency",
  "name": "GRAM ALTIN",
  "nameEn": "GRAM GOLD",
  "quantity": 50,
  "buyPrice": 5650.0,
  "createdAt": ISODate,
  "updatedAt": ISODate
}
```

## Frontend-Backend Integration Changes

### Files to Update:
1. **HomePage.js** - Replace mock data with API call to `/api/prices`
2. **PortfolioPage.js** - Replace mock data with API calls to `/api/portfolio`
3. **ConverterPage.js** - Use real-time prices from `/api/prices`

### Remove:
- AlertsPage.js (feature removed per user request)
- Alert-related mock data from mock.js
- Alerts tab from BottomNav.js

## Implementation Steps:
1. ✅ Create contracts.md
2. Remove alerts feature from frontend
3. Setup RapidAPI integration in backend
4. Create MongoDB models and routes
5. Update frontend to consume backend APIs
6. Test all features
