import asyncio
import logging
from celery import shared_task
from app.tasks.celery_app import celery_app
from app.clients.deribit import deribit_client
from app.db.database import AsyncSessionLocal
from app.db.models import CurrencyPrice

# Настройка логов, чтобы видеть процесс в Docker Desktop
logger = logging.getLogger(__name__)

async def save_prices_to_db():
    """
    Логика получения цен и сохранения в базу данных.
    """
    tickers = ["btc_usd", "eth_usd"]
    
    async with AsyncSessionLocal() as session:
        try:
            for ticker in tickers:
                logger.info(f"Fetching price for {ticker}...")
                data = await deribit_client.get_index_price(ticker)
                
                if data:
                    logger.info(f"Received data: {data}")
                    new_price = CurrencyPrice(
                        ticker=data["ticker"],
                        price=data["price"],
                        timestamp=data["timestamp"]
                    )
                    session.add(new_price)
                else:
                    logger.warning(f"Could not get data for {ticker}")
            
            await session.commit()
            logger.info("SUCCESS: All prices saved to crypto_db")
            return True
        except Exception as e:
            await session.rollback()
            logger.error(f"DATABASE ERROR during save: {e}")
            return False

@celery_app.task(name="app.tasks.worker.fetch_and_store_prices")
def fetch_and_store_prices():
    """
    Синхронная точка входа для Celery.
    """
    try:
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(save_prices_to_db())
    except Exception as e:
        logger.error(f"Worker task failed: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(save_prices_to_db())