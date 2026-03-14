from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.db.models import CurrencyPrice
from app.api.schemas import PriceResponse  

router = APIRouter(prefix="/prices", tags=["Prices"])

@router.get("/all", response_model=List[PriceResponse])
async def get_all_prices(
    ticker: Optional[str] = Query(None, description="Тикер валюты"),
    db: AsyncSession = Depends(get_db)
):
    query = select(CurrencyPrice)
    
    if ticker:  
        query = query.where(CurrencyPrice.ticker == ticker.lower())
    
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/latest", response_model=PriceResponse)
async def get_latest_price(
    ticker: str = Query(..., description="Тикер валюты"),
    db: AsyncSession = Depends(get_db)
):
    
    query = (
        select(CurrencyPrice)
        .where(CurrencyPrice.ticker == ticker.lower())
        .order_by(CurrencyPrice.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(query)
    price = result.scalar_one_or_none()
    if not price:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return price

@router.get("/history", response_model=List[PriceResponse])
async def get_price_history(
    ticker: str = Query(...),
    start_ts: int = Query(None, description="UNIX timestamp начала"),
    end_ts: int = Query(None, description="UNIX timestamp конца"),
    db: AsyncSession = Depends(get_db)
):
    
    query = select(CurrencyPrice).where(CurrencyPrice.ticker == ticker.lower())
    
    if start_ts:
        query = query.where(CurrencyPrice.timestamp >= start_ts)
    if end_ts:
        query = query.where(CurrencyPrice.timestamp <= end_ts)
        
    result = await db.execute(query)
    return result.scalars().all()