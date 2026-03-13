import aiohttp
import time

class DeribitClient:
    def __init__(self):
        self.base_url = "https://www.deribit.com/api/v2/public/get_index_price"

    async def get_index_price(self, ticker: str):
        index_name = ticker.lower().replace("-", "_")
    
        url = f"https://www.deribit.com/api/v2/public/get_index_price?index_name={index_name}"
    
    # Добавляем заголовки, чтобы прикинуться браузером
        headers = {'User-Agent': 'Mozilla/5.0'}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    data = await response.json()
                
                # Если всё ещё ошибка, мы увидим её в логах Docker
                    if "result" not in data:
                            print(f"!!! DERIBIT ERROR: {data}")
                            return None
                
                    return {
                        "ticker": ticker,
                        "price": data["result"]["index_price"],
                        "timestamp": int(time.time())
                    }
            except Exception as e:
                print(f"!!! CONNECTION ERROR: {e}")
            return None
        
    
    
    
# ВАЖНО: Создаем экземпляр здесь, чтобы воркер мог его импортировать
deribit_client = DeribitClient()