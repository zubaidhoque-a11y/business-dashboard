from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from database import Base


class Listing(Base):
    __tablename__ = "listing_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_name = Column(String(255), nullable=False)
    category = Column(String(100))
    city = Column(String(100))
    address = Column(Text)
    phone = Column(String(30))
    source = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
