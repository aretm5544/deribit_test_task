import pytest
from unittest.mock import patch
from app.clients.deribit import deribit_client

@pytest.mark.asyncio
async def test_deribit_client_success():
    
    mock_response = {
        "result": {"index_price": 72500.0}
    }
    
    with patch("aiohttp.ClientSession.get") as mocked_get:
        
        mocked_get.return_value.__aenter__.return_value.json.return_value = mock_response
        mocked_get.return_value.__aenter__.return_value.status = 200
        
        result = await deribit_client.get_index_price("btc_usd")
        
        assert result["ticker"] == "btc_usd"
        assert result["price"] == 72500.0
        assert "timestamp" in result