from .schemas import ItemCreate, UsageUpdate
from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException, Body
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.item import Item
from typing import Optional

router = APIRouter(prefix="/items", tags=["Items"])


# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Without HTML connection
# @router.post("/")
# def create_item(
#     name: str,
#     category: str,
#     cost: float,
#     purchase_date: date,
#     usage_start_date: date,
#     usage_end_date: date,
#     brand_name: str,
#     size: float,
#     size_unit: str,
#     db: Session = Depends(get_db)
# ):
#     new_item = Item(
#         name=name,
#         category=category,
#         cost=cost,
#         purchase_date=purchase_date,
#         usage_start_date=usage_start_date,
#         usage_end_date=usage_end_date,
#         brand_name=brand_name,
#         size=size,
#         size_unit=size_unit
#     )
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     return new_item

# With HTML connection
@router.post("/", response_model=dict)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(
        name=item.name,
        category=item.category,
        cost=item.cost,
        purchase_date=item.purchase_date,
        usage_start_date=item.usage_start_date,
        usage_end_date=item.usage_end_date,
        brand_name=item.brand_name,
        size=item.size,
        size_unit=item.size_unit
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item added successfully", "id": db_item.id}

# @router.get("/")
# def get_items(db: Session = Depends(get_db)):
#     items = db.query(Item).all()
#     return items

# # Without HTML connection
# @router.get("/filter")
# def get_items_filtered(
#     category: str | None = Query(None, description="Filter by category"),
#     brand_name: str | None = Query(None, description="Filter by brand"),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(Item)

#     if category:
#         query = query.filter(Item.category == category)
#     if brand_name:
#         query = query.filter(Item.brand_name == brand_name)

#     results = query.all()
#     return results

# With HTML connection
@router.get("/filter")
def get_items_filtered(
    category: Optional[str] = None,
    brand_name: Optional[str] = None,
    name: Optional[str] = None,
    purchase_start: Optional[date] = Query(None, description="Purchase date from"),
    purchase_end: Optional[date] = Query(None, description="Purchase date to"),
    usage_start_from: Optional[date] = Query(None, description="Usage start date from"),
    usage_start_to: Optional[date] = Query(None, description="Usage start date to"),
    db: Session = Depends(get_db)
):
    query = db.query(Item)

    if category:
        query = query.filter(Item.category == category)
    if brand_name:
        query = query.filter(Item.brand_name == brand_name)
    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))  # partial match

    if purchase_start:
        query = query.filter(Item.purchase_date >= purchase_start)
    if purchase_end:
        query = query.filter(Item.purchase_date <= purchase_end)

    if usage_start_from:
        query = query.filter(Item.usage_start_date >= usage_start_from)
    if usage_start_to:
        query = query.filter(Item.usage_start_date <= usage_start_to)

    results = query.all()
    return results

# Fetch single item by id
@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update usage dates
@router.put("/{item_id}/usage")
def update_usage_dates(
    item_id: int,
    usage: UsageUpdate = Body(...),  # <-- parse JSON body into UsageUpdate
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    print("Received start:", usage.usage_start_date)
    print("Received end:", usage.usage_end_date)

    if usage.usage_start_date:
        item.usage_start_date = usage.usage_start_date
    if usage.usage_end_date:
        item.usage_end_date = usage.usage_end_date

    db.commit()
    db.refresh(item)
    return item