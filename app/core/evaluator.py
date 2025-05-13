# Auto-generated file
import pandas as pd
from typing import Any, Dict, List

from app.core.indicator_config import INDICATOR_CATALOG
from app.core.evaluator_volume_patch import evaluate_volume_condition




def get_static_value(indicator: str, component: str) -> Any:
    """
    Fetch a static constant value like OVERBOUGHT, OVERSOLD if available.
    """
    entry = INDICATOR_CATALOG.get(indicator)
    if not entry:
        return None
    static_vals = entry.get("static_values", {})
    return static_vals.get(component)


def resolve_component_column(indicator: str, component: str, settings: Dict[str, Any]) -> str:
    """
    Dynamically resolve the column name for a given indicator and component
    based on INDICATOR_CATALOG settings.
    Falls back to component name directly if unknown.
    """
    config = INDICATOR_CATALOG.get(indicator)

    if not config:
        return component

    if indicator == "MACD":
        fast = int(settings.get("fast", 12))
        slow = int(settings.get("slow", 26))
        signal = int(settings.get("signal", 9))
        if component == "MACD_LINE":
            return f"MACD_{fast}_{slow}_{signal}"
        elif component == "SIGNAL_LINE":
            return f"MACDs_{fast}_{slow}_{signal}"
        elif component == "HISTOGRAM":
            return f"MACDh_{fast}_{slow}_{signal}"
        elif component == "ZERO_LINE":
            return "ZERO_LINE"

    if indicator == "PPO":
        fast = int(settings.get("fast", 12))
        slow = int(settings.get("slow", 26))
        signal = int(settings.get("signal", 9))
        if component == "PPO_LINE":
            return f"PPO_{fast}_{slow}_{signal}"
        elif component == "PPO_SIGNAL_LINE":
            return f"PPOs_{fast}_{slow}_{signal}"
        elif component == "ZERO_LINE":
            return "ZERO_LINE"

    if indicator == "BB":
        length = int(settings.get("length", 20))
        std = float(settings.get("std", 2.0))
        if component == "UPPER":
            return f"BBU_{length}_{std}"
        elif component == "LOWER":
            return f"BBL_{length}_{std}"
        elif component == "MIDDLE":
            return f"BBM_{length}_{std}"
        elif component in ["BANDWIDTH", "PERCENT_B"]:
            return f"{component}_{length}_{std}"

    if indicator in ["EMA", "SMA", "HMA", "WMA", "ZLMA", "SMMA", "DEMA", "TEMA"]:
        length = int(settings.get("length", 20))
        return f"{indicator}_{length}"

    if indicator == "RSI":
        length = int(settings.get("length", 14))
        if component == "RSI":
            return f"RSI_{length}"
        elif component == "RSI_MA":
            ma_period = int(settings.get("maPeriod", 10))
            return f"RSI_{length}_MA_{ma_period}"
        elif component in ["OVERBOUGHT", "OVERSOLD", "MIDDLE"]:
            return component

    if indicator == "ADX":
        length = int(settings.get("length", 14))
        return f"{component}_{length}"

    if indicator == "ATR":
        length = int(settings.get("length", 14))
        return f"ATR_{length}"

    if indicator == "DMI":
        length = int(settings.get("length", 14))
        return f"{component}_{length}"

    if indicator == "CCI":
        length = int(settings.get("length", 20))
        return f"CCI_{length}"

    if indicator == "MFI":
        length = int(settings.get("length", 14))
        return f"MFI_{length}"

    if indicator == "ROC":
        length = int(settings.get("length", 14))
        return f"ROC_{length}"

    if indicator == "Ultimate Oscillator":
        short = int(settings.get("short", 7))
        medium = int(settings.get("medium", 14))
        long = int(settings.get("long", 28))
        return f"UO_{short}_{medium}_{long}"

    if indicator == "TSI":
        short = int(settings.get("short", 13))
        long = int(settings.get("long", 25))
        return f"TSI_{short}_{long}"

    if indicator == "Vortex Indicator":
        length = int(settings.get("length", 14))
        return f"{component}_{length}"

    if indicator == "SuperTrend":
        length = int(settings.get("length", 10))
        multiplier = float(settings.get("multiplier", 3.0))
        return f"SUPERT_{length}_{multiplier}"

    if indicator == "Keltner Channels":
        ema = int(settings.get("ema", 20))
        atr = int(settings.get("atr", 10))
        mult = float(settings.get("mult", 2.0))
        return f"{component}_{ema}_{atr}_{mult}"

    if indicator == "Donchian Channels":
        lookback = int(settings.get("lookback", 20))
        return f"{component}_{lookback}"

    if indicator == "Ichimoku Cloud":
        tenkan = int(settings.get("tenkan", 9))
        kijun = int(settings.get("kijun", 26))
        senkou = int(settings.get("senkou", 52))
        return f"{component}_{tenkan}_{kijun}_{senkou}"

    return component


def extract_settings(condition: Dict[str, Any], indicator: str) -> Dict[str, Any]:
    config = INDICATOR_CATALOG.get(indicator, {})
    setting_keys = {s["key"] for s in config.get("settings", [])}
    settings = {}
    for key in setting_keys:
        val = condition.get(key)
        if val is not None and val != "":
            try:
                settings[key] = float(val)
            except:
                settings[key] = val
    return settings


def evaluate_condition(df: pd.DataFrame, condition: Dict[str, Any], timestamp: pd.Timestamp) -> bool:
    condition_type = condition.get("type", "indicator")

    if condition_type == "volume":
        result = evaluate_volume_condition(df, condition, timestamp)
        print(f"[DEBUG] Volume Condition @ {timestamp} ➜ {result}")
        return result

    if condition_type == "wick_ratio":
        lookback = int(condition.get("lookbackBars", 1))
        wick_side = condition.get("wickSide", "both").lower()
        ratio = float(condition.get("ratio", 0))

        idx = df.index.get_loc(timestamp)
        if idx - lookback < 0:
            return False

        row = df.iloc[idx - lookback]
        open_ = row["open"]
        close = row["close"]
        high = row["high"]
        low = row["low"]

        body = abs(close - open_)
        if body == 0:
            return False

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        if wick_side == "upper":
            return upper_wick >= body * ratio
        elif wick_side == "lower":
            return lower_wick >= body * ratio
        elif wick_side == "both":
            return upper_wick >= body * ratio and lower_wick >= body * ratio

        return False

    if condition_type == "ohlc":
        left = condition["leftOperand"]
        right_type = condition["rightOperandType"]
        right = condition["rightOperand"]
        operator = condition["operator"]
        lookback = int(condition.get("lookbackBars", 0))

        current_idx = df.index.get_loc(timestamp)
        if current_idx - lookback < 0:
            return False

        lhs_val = df.iloc[current_idx][left]

        if right == "ohlc4":
            ohlc4 = df.iloc[current_idx - lookback][["open", "high", "low", "close"]].mean()
            rhs_val = ohlc4
        elif right_type == "previous":
            rhs_val = df.iloc[current_idx - lookback][right]
        elif right_type in ["percent", "percentage_previous"]:
            prev_val = df.iloc[current_idx - lookback][left]
            percent = float(right if right_type == "percent" else condition.get("rightOperand", 0))
            rhs_val = prev_val * (1 + percent / 100)
        elif right_type == "static":
            rhs_val = float(condition.get("rightOperand", 0))
        else:
            rhs_val = df.iloc[current_idx][right]

        return compare_values(lhs_val, rhs_val, operator)

    if condition_type == "gap":
        lookback = int(condition.get("lookbackBars", 1))
        gap_size = float(condition.get("gapSize", 0))

        current_idx = df.index.get_loc(timestamp)
        if current_idx - lookback < 0:
            return False

        curr_open = df.iloc[current_idx]["open"]
        prev_close = df.iloc[current_idx - lookback]["close"]

        gap = ((curr_open - prev_close) / prev_close) * 100
        return gap >= gap_size

    if condition_type == "breakout":
        direction = condition.get("direction", "up")
        price = condition.get("price", "close")
        lookback = int(condition.get("lookbackBars", 5))

        current_idx = df.index.get_loc(timestamp)
        if current_idx - lookback < 0:
            return False

        past_window = df.iloc[current_idx - lookback:current_idx]
        current_price = df.iloc[current_idx][price]

        if direction == "up":
            highest = past_window["high"].max()
            return current_price > highest
        elif direction == "down":
            lowest = past_window["low"].min()
            return current_price < lowest

        return False

    if condition_type == "inside_bar":
        lookback = int(condition.get("lookbackBars", 1))
        current_idx = df.index.get_loc(timestamp)
        if current_idx - lookback < 1:
            return False

        current_high = df.iloc[current_idx - lookback]["high"]
        current_low = df.iloc[current_idx - lookback]["low"]
        prev_high = df.iloc[current_idx - lookback - 1]["high"]
        prev_low = df.iloc[current_idx - lookback - 1]["low"]

        return current_high < prev_high and current_low > prev_low

    if condition_type == "outside_bar":
        lookback = int(condition.get("lookbackBars", 1))
        current_idx = df.index.get_loc(timestamp)
        if current_idx - lookback < 1:
            return False

        current_high = df.iloc[current_idx - lookback]["high"]
        current_low = df.iloc[current_idx - lookback]["low"]
        prev_high = df.iloc[current_idx - lookback - 1]["high"]
        prev_low = df.iloc[current_idx - lookback - 1]["low"]

        return current_high > prev_high and current_low < prev_low

    # Default to indicator evaluation
    indicator = condition["indicator"]
    component = condition.get("component")
    operator = condition.get("operator")
    compare_with = condition.get("compareWith")
    settings = extract_settings(condition, indicator)

    col = resolve_component_column(indicator, component, settings)
    try:
        lhs = df.at[timestamp, col]
    except KeyError:
        print(f"[WARN] Column {col} not found in data at {timestamp}")
        return False

    if compare_with == "value":
        rhs = float(condition.get("compareValue"))
    elif compare_with == "indicator_component":
        rhs_component = condition.get("compareComponent")
        rhs_val = get_static_value(indicator, rhs_component)
        if rhs_val is not None:
            rhs = rhs_val
        else:
            rhs_col = resolve_component_column(indicator, rhs_component, settings)
            try:
                rhs = df.at[timestamp, rhs_col]
            except KeyError:
                print(f"[WARN] Compare column {rhs_col} not found")
                return False
    else:
        return False

    return compare_values(lhs, rhs, operator, df, timestamp, col)


def compare_values(lhs: float, rhs: float, operator: str, df: pd.DataFrame = None, timestamp: pd.Timestamp = None, col: str = None) -> bool:
    if operator == ">": return lhs > rhs
    if operator == "<": return lhs < rhs
    if operator == ">=": return lhs >= rhs
    if operator == "<=": return lhs <= rhs
    if operator == "==": return lhs == rhs
    if operator == "!=": return lhs != rhs

    if operator == "crosses_above":
        if df is None or timestamp is None or col is None:
            return False
        idx = df.index.get_loc(timestamp)
        if idx == 0:
            return False
        prev_lhs = df.iloc[idx - 1][col]
        return prev_lhs <= rhs and lhs > rhs

    if operator == "crosses_below":
        if df is None or timestamp is None or col is None:
            return False
        idx = df.index.get_loc(timestamp)
        if idx == 0:
            return False
        prev_lhs = df.iloc[idx - 1][col]
        return prev_lhs >= rhs and lhs < rhs

    return False



def evaluate_supporting_conditions(df: pd.DataFrame, groups: List[Dict[str, Any]], timestamp: pd.Timestamp) -> bool:
    if not groups:
        return True

    group_results = []
    for group in groups:
        group_logic = group.get("logicAfter", "AND").upper()
        if group_logic not in ["AND", "OR"]:
            group_logic = "AND"
        conditions = group.get("conditions", [])
        condition_results = [evaluate_condition(df, cond, timestamp) for cond in conditions]
        group_result = all(condition_results) if group_logic == "AND" else any(condition_results)
        group_results.append(group_result)

    return all(group_results)


def evaluate_entry_block(df: pd.DataFrame, block: Dict[str, Any], timestamp: pd.Timestamp) -> bool:
    main = block.get("mainCondition")
    support = block.get("supportingConditions", [])
    logic = block.get("internalLogic", "AND")
    max_bars_after_support = block.get("maxBarsAfterSupport", 0)

    if not main and not support:
        return False

    # If maxBarsAfterSupport is 0 or missing ➔ behave as usual (support + main same bar)
    if not max_bars_after_support:
        main_result = evaluate_condition(df, main, timestamp) if main else True
        support_result = evaluate_supporting_conditions(df, support, timestamp)
        print(f"[DEBUG] Entry Check @ {timestamp} ➔ MAIN={main_result} SUPPORT={support_result}")

        if logic == "AND":
            return main_result and support_result
        if logic == "OR":
            return main_result or support_result

        return False

    # New logic: support first, then wait for main
    support_result = evaluate_supporting_conditions(df, support, timestamp)

    if not support_result:
        # If supporting conditions not satisfied, skip
        return False

    # Supporting satisfied ➔ now check for main within next max_bars_after_support
    start_idx = df.index.get_loc(timestamp)
    end_idx = start_idx + max_bars_after_support

    if end_idx >= len(df.index):
        end_idx = len(df.index) - 1

    for idx in range(start_idx, end_idx + 1):
        ts = df.index[idx]
        main_result = evaluate_condition(df, main, ts) if main else True
        if main_result:
            print(f"[DEBUG] Main condition triggered @ {ts} within {max_bars_after_support} bars after support.")
            return True

    # Main did not trigger in allowed bars
    print(f"[DEBUG] Support true at {timestamp}, but main condition NOT triggered within {max_bars_after_support} bars.")
    return False

