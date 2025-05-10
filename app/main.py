from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils.supabase_client import supabase

app = FastAPI()

@app.get("/strategies")
async def get_strategies():
    try:
        response = supabase.table("strategies").select("*").execute()
        if response.error:
            raise Exception(response.error)
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
