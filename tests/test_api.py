import pytest

@pytest.mark.asyncio
async def test_get_all_prices_empty(ac):
    """Проверка, что изначально список цен пуст"""
    response = await ac.get("/prices/all")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_prices_by_ticker(ac):
    """Проверка фильтрации (даже если данных нет, эндпоинт должен вернуть 200)"""
    response = await ac.get("/prices/all?ticker=btc_usd")
    assert response.status_code == 200