from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import func, insert, select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Listing

# Creates the table automatically if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Listings API")

# Allow the React app (Vite runs on 5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Schemas ----------
class ListingIn(BaseModel):
    business_name: str
    category: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = None


# ---------- Helpers ----------
def count_by(db: Session, column, label: str):
    """SELECT <column>, COUNT(*) FROM listing_master GROUP BY <column>"""
    rows = db.execute(
        select(column, func.count().label("count"))
        .group_by(column)
        .order_by(func.count().desc())
    ).all()
    return [{label: (r[0] or "Unknown"), "count": r[1]} for r in rows]


# ---------- APIs ----------
@app.get("/")
def root():
    return {"message": "Business Listings API is running. See /docs"}


@app.post("/listings/bulk")
def insert_listings(listings: List[ListingIn], db: Session = Depends(get_db)):
    """Bulk insert scraped listings into MySQL."""
    if not listings:
        return {"inserted": 0}
    db.execute(insert(Listing), [l.model_dump() for l in listings])
    db.commit()
    return {"inserted": len(listings)}


@app.get("/stats/city")
def city_stats(db: Session = Depends(get_db)):
    return count_by(db, Listing.city, "city")


@app.get("/stats/category")
def category_stats(db: Session = Depends(get_db)):
    return count_by(db, Listing.category, "category")


@app.get("/stats/source")
def source_stats(db: Session = Depends(get_db)):
    return count_by(db, Listing.source, "source")


@app.get("/stats/total")
def total(db: Session = Depends(get_db)):
    return {"total": db.scalar(select(func.count()).select_from(Listing))}
