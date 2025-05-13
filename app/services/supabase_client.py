# Auto-generated file
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Supabase credentials are missing in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_strategies():
    response = supabase.table("strategies").select("*").execute()
    if response.error:
        raise Exception(f"❌ Error fetching strategies: {response.error.message}")
    return response.data
