from fastapi import APIRouter, HTTPException
from app.utils.supabase_client import supabase

router = APIRouter()

@router.get("/", name="Get Strategies")
async def get_strategies():
    try:
        response = supabase.table("strategies").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to fetch strategies: {e}")
