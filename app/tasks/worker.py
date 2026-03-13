import asyncio
from app.tasks.celery_app import celery_app
from app.clients.deribit import deribit_client
from app.db.database import AsyncSessionLocal
from app.db.models import CurrencyPrice

@celery_app.task
def fetch_and_store_prices():
    """
    Синхронная обертка для асинхронной задачи сбора цен.
    """
    return asyncio.run(run_fetch_prices())

async def run_fetch_prices():
    tickers = ["btc_usd", "eth_usd"] 
    
    async with AsyncSessionLocal() as session:
        for ticker in tickers:
            
            data = await deribit_client.get_index_price(ticker)
            
            
            new_price = CurrencyPrice(
                ticker=data["ticker"],
                price=data["price"],
                timestamp=data["timestamp"]
            )
            session.add(new_price)
        
        await session.commit()