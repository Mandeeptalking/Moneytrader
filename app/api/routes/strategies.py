from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime

from app.services.supabase_client import supabase

router = APIRouter()


# ✅ Strategy Input Schema
class Condition(BaseModel):
    indicator: str
    component: str
    operator: str
    compareWith: str
    compareValue: Optional[float] = None
    compareComponent: Optional[str] = None
    settings: Optional[Dict[str, Any]] = {}


class StrategyCreateRequest(BaseModel):
    strategy_name: str
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    entry_conditions: Dict[str, Any]
    strategy_behavior: Optional[Dict[str, Any]] = {}
    exit_rules: Optional[Dict[str, Any]] = None
    add_to_position: Optional[Dict[str, Any]] = None
    order_config: Dict[str, Any]
    stop_loss_config: Optional[Dict[str, Any]] = None
    take_profit_config: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    summary: Optional[str] = None


# ✅ POST /strategies → Save Strategy to Supabase
@router.post("")
async def create_strategy(strategy: StrategyCreateRequest, request: Request):
    try:
        new_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        record = {
            "id": new_id,
            "user_id": "public_user",  # 🔒 Replace with real auth later
            "strategy_name": strategy.strategy_name,
            "symbol": strategy.symbol,
            "timeframe": strategy.timeframe,
            "start_date": strategy.start_date,
            "end_date": strategy.end_date,
            "entry_conditions": strategy.entry_conditions,
            "strategy_behavior": strategy.strategy_behavior,
            "exit_rules": strategy.exit_rules,
            "add_to_position": strategy.add_to_position,
            "order_config": strategy.order_config,
            "stop_loss_config": strategy.stop_loss_config,
            "take_profit_config": strategy.take_profit_config,
            "notes": strategy.notes,
            "summary": strategy.summary or f"Strategy for {strategy.symbol} using {strategy.timeframe} timeframe",
            "created_at": now,
            "updated_at": now
        }

        response = supabase.table("strategies").insert(record).execute()
        if response.data:
            return {"message": "✅ Strategy saved", "strategy_id": new_id}
        else:
            raise HTTPException(status_code=500, detail="❌ Failed to save strategy")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error: {e}")


# ✅ GET /strategies → Fetch all strategies
@router.get("")
async def get_strategies():
    try:
        response = supabase.table("strategies").select("*").order("created_at", desc=True).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="No strategies found")
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to fetch strategies: {e}")


# ✅ GET /strategies/{id} → Fetch single strategy
@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str):
    try:
        response = supabase.table("strategies").select("*").eq("id", strategy_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Strategy not found")
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to fetch strategy: {e}")
