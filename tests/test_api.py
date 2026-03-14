import pytest
from httpx import AsyncClient, ASGITransport 
from app.main import app


@pytest.fixture
async def ac():
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_all_prices_empty(ac):
    """Проверка получения списка цен"""
    response = await ac.get("/prices/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_prices_by_ticker(ac):
    """Проверка фильтрации (даже если данных нет, эндпоинт должен вернуть 200)"""
    response = await ac.get("/prices/all?ticker=btc_usd")
    assert response.status_code == 200