from pydantic import BaseModel
from datetime import date
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    category: str
    cost: float
    purchase_date: Optional[date] = None
    usage_start_date: Optional[date] = None
    usage_end_date: Optional[date] = None
    brand_name: Optional[str] = None
    size: Optional[float] = None
    size_unit: Optional[str] = None

class UsageUpdate(BaseModel):
    usage_start_date: Optional[date] = None
    usage_end_date: Optional[date] = None
