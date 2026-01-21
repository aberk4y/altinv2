from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime, timedelta

# Load environment variables BEFORE importing services
ROOT_DIR = Path(__file__).parent
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
import asyncio

from models import PortfolioItem, PortfolioItemCreate, PortfolioItemUpdate, User, Margin
from harem_api_service import harem_api_service
from auth_service import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Auth config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/admin/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Simple check - in prod verify signature and user existence
    # We trust auth_service.verify_token if implemented, otherwise here generic check
    # For now, let's just use the existence of token as "logged in" for simplicity or implement proper verify
    # Re-implementing verify here for safety using auth_service logic
    from jose import jwt, JWTError
    from auth_service import SECRET_KEY, ALGORITHM
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Root endpoint
@api_router.get("/")
async def root():
    return {"message": "Berkay Altın API"}

# --- ADMIN AUTH ---
@api_router.post("/admin/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/admin/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user["username"], "is_active": current_user["is_active"]}

# --- MARGINS ---
@api_router.get("/margins", response_model=List[Margin])
async def get_margins(current_user: User = Depends(get_current_user)):
    margins = await db.margins.find({}).to_list(1000)
    return [Margin(**m) for m in margins]

@api_router.post("/margins", response_model=Margin)
async def update_margin(margin: Margin, current_user: User = Depends(get_current_user)):
    # Update if exists, insert if not
    await db.margins.update_one(
        {"product_name_key": margin.product_name_key},
        {"$set": margin.dict(exclude={"id"})},
        upsert=True
    )
    updated = await db.margins.find_one({"product_name_key": margin.product_name_key})
    return Margin(**updated)

# --- PRICES (WITH MARGINS) ---
@api_router.get("/prices")
async def get_prices(type: Optional[str] = "all"):
    """Get real-time gold and currency prices from Harem Altın API with Margins Applied"""
    try:
        # 1. Fetch real prices (run blocking IO in thread)
        prices_data = await asyncio.to_thread(harem_api_service.get_all_prices)
        
        # 2. Fetch margins from DB
        # Convert to dict for O(1) checking: {"GRAM ALTIN": {amount: 5, is_percentage: False}}
        margins_list = await db.margins.find({}).to_list(1000)
        margins_map = {m["product_name_key"]: m for m in margins_list}
        
        # 3. Apply margins
        def apply_margin(items):
            for item in items:
                key = item.get("name") # "GRAM ALTIN"
                if key in margins_map:
                    margin_data = margins_map[key]
                    amount = margin_data["margin_amount"]
                    is_percent = margin_data.get("is_percentage", False)
                    
                    if is_percent:
                        # Percentage logic (e.g. 5%)
                        # Buy - 5%, Sell + 5%
                        margin_buy = item["buy"] * (amount / 100)
                        margin_sell = item["sell"] * (amount / 100)
                        item["buy"] -= margin_buy
                        item["sell"] += margin_sell
                    else:
                        # Fixed amount logic (e.g. 5 TL)
                        item["buy"] -= amount
                        item["sell"] += amount
                        
                    # Rounding
                    item["buy"] = round(item["buy"], 2)
                    item["sell"] = round(item["sell"], 2)
            return items

        result = {
            "lastUpdate": datetime.utcnow().isoformat()
        }
        
        if type in ["all", "gold"]:
            gold_items = prices_data.get("gold", [])
            result["gold"] = apply_margin(gold_items)
        
        if type in ["all", "currency"]:
            currency_items = prices_data.get("currency", [])
            result["currency"] = apply_margin(currency_items)
        
        return result
    except Exception as e:
        logging.error(f"Error fetching prices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Portfolio Management
@api_router.post("/portfolio", response_model=PortfolioItem)
async def create_portfolio_item(item: PortfolioItemCreate):
    """Create new portfolio item"""
    try:
        portfolio_item = PortfolioItem(**item.dict())
        await db.portfolio.insert_one(portfolio_item.dict())
        return portfolio_item
    except Exception as e:
        logging.error(f"Error creating portfolio item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/portfolio", response_model=List[PortfolioItem])
async def get_portfolio():
    """Get all portfolio items"""
    try:
        items = await db.portfolio.find({"userId": "default"}).to_list(1000)
        return [PortfolioItem(**item) for item in items]
    except Exception as e:
        logging.error(f"Error fetching portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/portfolio/{item_id}", response_model=PortfolioItem)
async def update_portfolio_item(item_id: str, update: PortfolioItemUpdate):
    """Update portfolio item"""
    try:
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        result = await db.portfolio.find_one_and_update(
            {"id": item_id, "userId": "default"},
            {"$set": update_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Portfolio item not found")
        
        return PortfolioItem(**result)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating portfolio item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/portfolio/{item_id}")
async def delete_portfolio_item(item_id: str):
    """Delete portfolio item"""
    try:
        result = await db.portfolio.delete_one({"id": item_id, "userId": "default"})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Portfolio item not found")
        
        return {"message": "Portfolio item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting portfolio item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

origins = os.environ.get('CORS_ORIGINS', '').split(',')
if not origins or origins == ['']:
    origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8001"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()