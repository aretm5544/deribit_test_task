from fastapi import FastAPI
from app.api.routes import router as prices_router

app = FastAPI(
    title="Crypto Price Tracker API",
    description="API для отслеживания курсов BTC и ETH с биржи Deribit",
    version="1.0.0"
)


app.include_router(prices_router)

@app.get("/")
async def root():
    return {"message": "API is running. Go to /docs for swagger documentation."}
