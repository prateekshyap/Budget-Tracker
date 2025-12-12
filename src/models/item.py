from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    cost = Column(Float)
    purchase_date = Column(Date)
    usage_start_date = Column(Date)
    usage_end_date = Column(Date)
    brand_name = Column(String, index=True)
    size = Column(Float)
    size_unit = Column(String)
