# app/api/routes/backtest.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
import pandas as pd

from app.services.supabase_client import supabase
from app.core.data_loader import load_hybrid_data
from app.core.backtest_engine import simulate_strategy
from app.core.indicator_engine import apply_flat_indicators



router = APIRouter()

@router.post("/{strategy_id}")
async def run_backtest_for_strategy(strategy_id: str):
    try:
        # ✅ Fetch strategy from Supabase
        response = supabase.table("strategies").select("*").eq("id", strategy_id).single().execute()
        strategy = response.data

        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        symbol = strategy.get("symbol")
        timeframe = strategy.get("timeframe")
        start = strategy.get("start_date")
        end = strategy.get("end_date")
        capital = strategy.get("order_config", {}).get("capital", 100000)

        if not (symbol and timeframe and start and end):
            raise HTTPException(status_code=400, detail="Missing symbol, timeframe, or dates")

        # ✅ Convert date strings to datetime
        start_date = pd.to_datetime(start, utc=True)
        end_date = pd.to_datetime(end, utc=True)

        # ✅ Load historical OHLCV data
        df = load_hybrid_data(symbol, timeframe, start_date, end_date)
        if df.empty:
            raise HTTPException(status_code=400, detail="No OHLCV data found for selected range")

        # ✅ Apply indicators before evaluation
        df = apply_flat_indicators(df, strategy["entry_conditions"])

        # ✅ Run simulation
        results = simulate_strategy(df, strategy, initial_capital=float(capital))

        return {
            "message": f"✅ Backtest completed for {strategy['strategy_name']}",
            "symbol": symbol,
            "timeframe": timeframe,
            "start": start,
            "end": end,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Backtest failed: {str(e)}")
