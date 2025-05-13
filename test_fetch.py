# test_fetch.py

from app.utils.supabase_client import supabase

def fetch_strategies():
    try:
        response = supabase.table("strategies").select("*").execute()
        print("RESPONSE:", response)
        print("\nDATA:", response.data)
    except Exception as e:
        print(f"❌ Error fetching strategies: {e}")

if __name__ == "__main__":
    fetch_strategies()
