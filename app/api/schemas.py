from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PriceResponse(BaseModel):
    
    ticker: str
    price: Decimal  
    timestamp: int

    
    model_config = ConfigDict(from_attributes=True)