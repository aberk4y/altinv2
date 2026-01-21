from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
import uuid

class PortfolioItemCreate(BaseModel):
    type: Literal['gold', 'currency']
    name: str
    nameEn: str
    quantity: float
    buyPrice: float

class PortfolioItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str = "default"
    type: Literal['gold', 'currency']
    name: str
    nameEn: str
    quantity: float
    buyPrice: float
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class PortfolioItemUpdate(BaseModel):
    quantity: Optional[float] = None
    buyPrice: Optional[float] = None

class User(BaseModel):
    username: str
    hashed_password: str
    is_active: bool = True

class Margin(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_name_key: str # e.g. "GRAM ALTIN" or "USDTRY"
    margin_amount: float # Standard margin (spread widening)
    margin_buy: float = 0.0 # Extra adjustment for Buy Price (+/-)
    margin_sell: float = 0.0 # Extra adjustment for Sell Price (+/-)
    is_percentage: bool = False
    is_visible: bool = True # Show/Hide product on user frontend
    updated_at: datetime = Field(default_factory=datetime.utcnow)
