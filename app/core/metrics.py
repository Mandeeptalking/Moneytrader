# Auto-generated file
import pandas as pd
import numpy as np
from typing import List, Dict, Any

def calculate_metrics(trades: List[Dict[str, Any]], starting_capital: float, final_capital: float) -> Dict[str, Any]:
    if not trades:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0.0,
            "pnl": 0.0,
            "final_capital": final_capital,
            "starting_capital": starting_capital,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0
        }

    sell_trades = [t for t in trades if t["type"].startswith("SELL")]
    pnl_values = [t.get("pnl", 0) for t in sell_trades]

    wins = sum(1 for pnl in pnl_values if pnl > 0)
    losses = sum(1 for pnl in pnl_values if pnl <= 0)
    total = len(pnl_values)
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0.0
    pnl = round(final_capital - starting_capital, 2)

    equity_curve = build_equity_curve(trades, starting_capital)
    sharpe = calculate_sharpe_ratio(equity_curve)
    drawdown = calculate_max_drawdown(equity_curve)

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "pnl": pnl,
        "final_capital": final_capital,
        "starting_capital": starting_capital,
        "sharpe_ratio": round(sharpe, 3),
        "max_drawdown": round(drawdown, 2)
    }

def build_equity_curve(trades: List[Dict[str, Any]], starting_capital: float) -> pd.Series:
    capital = starting_capital
    curve = []
    for t in trades:
        if t["type"].startswith("SELL"):
            pnl = t.get("pnl", 0)
            capital += pnl
        curve.append(capital)
    return pd.Series(curve)

def calculate_sharpe_ratio(equity: pd.Series) -> float:
    returns = equity.pct_change().dropna()
    if returns.std() == 0 or len(returns) < 2:
        return 0.0
    return (returns.mean() / returns.std()) * np.sqrt(252)

def calculate_max_drawdown(equity: pd.Series) -> float:
    cumulative_max = equity.cummax()
    drawdown = (equity - cumulative_max) / cumulative_max
    return drawdown.min() * 100
