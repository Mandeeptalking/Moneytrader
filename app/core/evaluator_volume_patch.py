import pandas as pd
from typing import Dict

def evaluate_volume_condition(df: pd.DataFrame, condition: Dict, timestamp: pd.Timestamp) -> bool:
    """
    Evaluate volume-based condition using raw volume values.

    Supported operators:
      >, <, >=, <=, ==, !=, crosses_above, crosses_below

    Condition structure:
    {
        "type": "volume",
        "operator": ">",
        "compareWith": "value" | "volume_column",
        "compareValue": 500000, (if compareWith = value)
        "compareColumn": "volume" (optional, default: volume)
    }
    """
    operator = condition.get("operator")
    compare_with = condition.get("compareWith", "value")
    column = condition.get("compareColumn", "volume")

    try:
        lhs = df.at[timestamp, column]
    except KeyError:
        print(f"[WARN] Volume column '{column}' not found at {timestamp}")
        return False

    if compare_with == "value":
        try:
            rhs = float(condition.get("compareValue", 0))
        except:
            return False
    elif compare_with == "volume_column":
        rhs_column = condition.get("compareColumn", "volume")
        try:
            rhs = df.at[timestamp, rhs_column]
        except KeyError:
            print(f"[WARN] RHS column '{rhs_column}' not found at {timestamp}")
            return False
    else:
        return False

    if operator == ">": return lhs > rhs
    if operator == "<": return lhs < rhs
    if operator == ">=": return lhs >= rhs
    if operator == "<=": return lhs <= rhs
    if operator == "==": return lhs == rhs
    if operator == "!=": return lhs != rhs

    if operator == "crosses_above":
        prev_idx = df.index.get_loc(timestamp) - 1
        if prev_idx < 0: return False
        prev_lhs = df.iloc[prev_idx][column]
        return prev_lhs < rhs and lhs > rhs

    if operator == "crosses_below":
        prev_idx = df.index.get_loc(timestamp) - 1
        if prev_idx < 0: return False
        prev_lhs = df.iloc[prev_idx][column]
        return prev_lhs > rhs and lhs < rhs

    return False
