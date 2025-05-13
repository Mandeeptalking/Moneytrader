from fastapi import FastAPI
from app.api.routes import backtest, strategies

app = FastAPI(title="Trading Backend API")

# Notice: no extra /strategies here; it will be handled inside strategies.py
app.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])

@app.get("/")
async def root():
    return {"message": "🚀 Trading Backend API is running"}
