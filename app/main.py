from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Add this import
from app.api.routes import backtest, strategies

app = FastAPI(title="Trading Backend API")

# ✅ Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.deally.in"],  # Your live frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])

@app.get("/")
async def root():
    return {"message": "🚀 Trading Backend API is running"}
