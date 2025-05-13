# Auto-generated file
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple
from app.utils.supabase_client import supabase

def get_available_range(symbol: str, timeframe: str) -> Optional[Tuple[datetime, datetime]]:
    """
    Fetch available start and end dates for a symbol and timeframe from Supabase.
    """
    response = (
        supabase.table("distinct_symbol_timeframes")
        .select("start_date, end_date")
        .eq("symbol", symbol)
        .eq("timeframe", timeframe)
        .limit(1)
        .execute()
    )

    data = response.data
    if not data:
        return None

    start = pd.to_datetime(data[0]["start_date"], utc=True)
    end = pd.to_datetime(data[0]["end_date"], utc=True)
    return start, end

def fetch_ohlcv(symbol: str, timeframe: str, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV bars from 'historical_indian_stocks' table in Supabase.
    """
    all_rows = []
    page_size = 1000
    offset = 0

    while True:
        response = (
            supabase.table("historical_indian_stocks")
            .select("datetime, open, high, low, close, volume")
            .eq("symbol", symbol)
            .eq("timeframe", timeframe)
            .gte("datetime", start_date.isoformat())
            .lte("datetime", end_date.isoformat())
            .order("datetime", desc=False)
            .range(offset, offset + page_size - 1)
            .execute()
        )

        rows = response.data
        if not rows:
            break

        all_rows.extend(rows)

        if len(rows) < page_size:
            break

        offset += page_size

    if not all_rows:
        print(f"[WARN] No OHLCV data found for {symbol} [{timeframe}] between {start_date} and {end_date}")
        return None

    df = pd.DataFrame(all_rows)

    if df.empty:
        return None

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df.set_index("datetime", inplace=True)
    df.sort_index(inplace=True)

    return df

def load_hybrid_data(symbol: str, timeframe: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Load data for a Hybrid Strategy backtest. Includes range validation.
    """
    available_range = get_available_range(symbol, timeframe)
    if not available_range:
        print(f"[ERROR] No available data for {symbol} [{timeframe}]")
        return pd.DataFrame()

    available_start, available_end = available_range
    print(f"[DEBUG] Available data range: {available_start.date()} to {available_end.date()}")

    if end_date < available_start or start_date > available_end:
        print(f"[ERROR] Requested range is outside available historical data.")
        return pd.DataFrame()

    if start_date.tzinfo is None:
        start_date = start_date.tz_localize('UTC')
    if end_date.tzinfo is None:
        end_date = end_date.tz_localize('UTC')

    df = fetch_ohlcv(symbol, timeframe, start_date, end_date)
    if df is None or df.empty:
        print(f"[ERROR] No rows fetched for {symbol} [{timeframe}]")
        return pd.DataFrame()

    print(f"\n✅ Loaded {len(df)} rows from {df.index.min()} to {df.index.max()}")
    return df
