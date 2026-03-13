from sqlalchemy import BigInteger, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class CurrencyPrice(Base):
    __tablename__ = "currency_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Тикер валюты (например, BTC-USD) 
    ticker: Mapped[str] = mapped_column(String(20), index=True)
    # Цена (используем Numeric для точности финансовых данных) 
    price: Mapped[float] = mapped_column(Numeric(precision=18, scale=8))
    # Время в UNIX timestamp 
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)