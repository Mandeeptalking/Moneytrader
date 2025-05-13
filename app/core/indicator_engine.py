# Auto-generated file
import pandas as pd
import pandas_ta as ta
from app.core.indicator_config import INDICATOR_CATALOG

def apply_flat_indicators(df: pd.DataFrame, entry_conditions: dict) -> pd.DataFrame:
    """
    Apply indicators based on a flat strategy format with main_condition and supporting_conditions.
    """
    if df is None or df.empty:
        print("[ERROR] Cannot apply indicators to empty dataframe.")
        return df

    applied_keys = set()

    # Main condition
    main = entry_conditions.get("main_condition")
    if main and main.get("indicator"):
        df = apply_single_indicator(df, main, applied_keys)

    # Supporting conditions
    for cond in entry_conditions.get("supporting_conditions", []):
        if cond.get("indicator"):
            df = apply_single_indicator(df, cond, applied_keys)

    return df

def apply_single_indicator(df: pd.DataFrame, condition: dict, applied_keys: set) -> pd.DataFrame:
    indicator_name = condition.get("indicator")
    config = INDICATOR_CATALOG.get(indicator_name)

    if not config:
        print(f"[WARN] Unknown indicator: {indicator_name}")
        return df

    ta_func = config.get("pandas_ta")
    settings = extract_settings(condition, config)

    if "period" in condition and "length" not in settings:
        settings["length"] = float(condition["period"])

    if indicator_name == "MACD":
        settings.setdefault("fast", 12)
        settings.setdefault("slow", 26)
        settings.setdefault("signal", 9)

    key = (indicator_name, tuple(sorted(settings.items())))
    if key in applied_keys:
        return df

    try:
        if not ta_func or not hasattr(ta, ta_func):
            print(f"[WARN] pandas-ta has no function '{ta_func}' for {indicator_name}.")
            return df

        ta_function = getattr(ta, ta_func)
        df_ind = None

        if ta_func in ["macd", "bbands", "adx", "kc", "donchian"]:
            df_ind = ta_function(df["close"], **settings)
        else:
            df_ind = ta_function(df["close"], **settings)

        if df_ind is not None and not df_ind.empty:
            df = df.join(df_ind)
            applied_keys.add(key)
            print(f"[INFO] Applied {indicator_name} with {settings}")
        else:
            print(f"[WARN] {indicator_name} returned empty output.")

    except Exception as e:
        print(f"[ERROR] Failed to apply {indicator_name} with {settings}: {e}")

    return df

def extract_settings(condition: dict, config: dict) -> dict:
    valid_keys = {s["key"] for s in config.get("settings", [])}
    extracted = {}

    for key in valid_keys:
        val = condition.get(key)
        if val is None and isinstance(condition.get("config"), dict):
            val = condition["config"].get(key)
        if val is None and key == "length" and condition.get("period"):
            val = condition.get("period")

        if val is not None and val != "":
            try:
                extracted[key] = float(val)
            except ValueError:
                extracted[key] = val

    return extracted
