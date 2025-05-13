import pandas as pd
from typing import Dict, Any, List
from app.core.evaluator import evaluate_condition, evaluate_supporting_conditions
from app.core.metrics import calculate_metrics

def simulate_strategy(
    df: pd.DataFrame,
    strategy: Dict[str, Any],
    initial_capital: float = 100000.0
) -> Dict[str, Any]:
    capital = initial_capital
    positions: List[Dict[str, Any]] = []
    trades = []
    adds_done = 0
    total_commission = 0.0

    atp_triggered = 0
    atp_executed = 0
    atp_skipped_reasons = {
        "insufficient_capital": 0,
        "invalid_qty": 0,
        "max_adds_reached": 0
    }

    blocks = strategy.get("blocks", [])
    stop_config = strategy.get("stopLoss", {})
    take_profit_config = strategy.get("takeProfit", {})
    add_position_config = strategy.get("addPosition", {})

    cooldown_bars = take_profit_config.get("cooldownBars", 0)
    next_entry_allowed_index = 0

    raw_commission = strategy.get("commission", 0.077)
    try:
        commission_rate = float(raw_commission) / 100
    except (ValueError, TypeError):
        print(f"[WARN] Invalid commission value '{raw_commission}', falling back to 0.077%")
        commission_rate = 0.077 / 100

    add_capital_pool = float(add_position_config.get("capitalPool", 0))
    remaining_add_capital = add_capital_pool

    for i, ts in enumerate(df.index):
        price = df.at[ts, "close"]

        if positions:
            total_qty = sum(p["quantity"] for p in positions)
            exited_qty = 0

            if take_profit_config.get("enabled"):
                for rule in take_profit_config.get("conditions", []):
                    if rule["type"] == "percentage":
                        target_pct = float(rule["value"])
                        exit_size_pct = rule.get("exitSize", 100)
                        exit_qty = int(total_qty * exit_size_pct / 100)
                        to_exit = []

                        for pos in positions:
                            pnl_pct = (price - pos["entry_price"]) / pos["entry_price"] * 100
                            if pnl_pct >= target_pct and exit_qty > 0:
                                qty_to_exit = min(pos["quantity"], exit_qty)
                                to_exit.append((pos, qty_to_exit))
                                exit_qty -= qty_to_exit

                        if to_exit:
                            for pos, qty in to_exit:
                                pnl = round((price - pos["entry_price"]) * qty, 2)
                                turnover = (pos["entry_price"] + price) * qty
                                commission = round(turnover * commission_rate, 2)
                                total_commission += commission

                                trades.append({
                                    "type": "SELL-TP",
                                    "time": ts,
                                    "price": price,
                                    "details": rule,
                                    "quantity": qty,
                                    "entry_price": pos["entry_price"],
                                    "pnl": pnl,
                                    "commission": commission
                                })
                                capital += price * qty
                                pos["quantity"] -= qty
                                exited_qty += qty

                            positions = [p for p in positions if p["quantity"] > 0]

                            if not positions:
                                next_entry_allowed_index = i + cooldown_bars
                            break

            if positions and stop_config.get("enabled"):
                for rule in stop_config.get("conditions", []):
                    if rule["type"] == "percentage":
                        threshold_pct = float(rule["value"])
                        to_exit = []

                        for pos in positions:
                            pnl_pct = (price - pos["entry_price"]) / pos["entry_price"] * 100
                            if pnl_pct <= -threshold_pct:
                                to_exit.append(pos)

                        if to_exit:
                            for pos in to_exit:
                                qty = pos["quantity"]
                                pnl = round((price - pos["entry_price"]) * qty, 2)
                                turnover = (pos["entry_price"] + price) * qty
                                commission = round(turnover * commission_rate, 2)
                                total_commission += commission

                                trades.append({
                                    "type": "SELL-SL",
                                    "time": ts,
                                    "price": price,
                                    "details": rule,
                                    "quantity": qty,
                                    "entry_price": pos["entry_price"],
                                    "pnl": pnl,
                                    "commission": commission
                                })
                                capital += price * qty
                                pos["quantity"] = 0

                            positions = [p for p in positions if p["quantity"] > 0]

                            if not positions:
                                next_entry_allowed_index = i + cooldown_bars
                            break

            if positions and add_position_config.get("enabled"):
                if adds_done >= add_position_config.get("maxAdds", 0):
                    atp_skipped_reasons["max_adds_reached"] += 1
                else:
                    last_entry = positions[-1]
                    entry_price = last_entry["entry_price"]
                    for rule in add_position_config.get("conditions", []):
                        if rule["type"] == "price_drop_percent":
                            drop_pct = float(rule["value"])
                            pct_change = (price - entry_price) / entry_price * 100

                            if pct_change <= -drop_pct:
                                atp_triggered += 1

                                add_value = float(rule["addValue"])
                                qty_to_add = int(add_value // price)
                                total_cost = qty_to_add * price

                                if qty_to_add <= 0:
                                    atp_skipped_reasons["invalid_qty"] += 1
                                    continue

                                if remaining_add_capital >= total_cost:
                                    new_position = {
                                        "entry_time": ts,
                                        "entry_price": price,
                                        "quantity": qty_to_add,
                                        "capital_used": total_cost
                                    }
                                    positions.append(new_position)
                                    remaining_add_capital -= total_cost
                                    adds_done += 1
                                    atp_executed += 1
                                    trades.append({
                                        "type": "ADD",
                                        "time": ts,
                                        "price": price,
                                        "details": rule,
                                        "quantity": qty_to_add
                                    })
                                else:
                                    atp_skipped_reasons["insufficient_capital"] += 1

        if not positions and i >= next_entry_allowed_index:
            for block in blocks:
                main = block.get("mainCondition")
                supports = block.get("supportingConditions", [])

                main_pass = evaluate_condition(df, main, ts)
                support_pass = evaluate_supporting_conditions(df, supports, ts)

                if main_pass and support_pass:
                    qty = int(capital // price)
                    if qty == 0:
                        continue
                    new_position = {
                        "entry_time": ts,
                        "entry_price": price,
                        "quantity": qty,
                        "capital_used": qty * price
                    }
                    positions.append(new_position)
                    capital -= qty * price
                    trades.append({
                        "type": "BUY",
                        "time": ts,
                        "price": price,
                        "details": new_position
                    })
                    break

    if positions:
        final_price = df.at[df.index[-1], "close"]
        for pos in positions:
            qty = pos["quantity"]
            pnl = round((final_price - pos["entry_price"]) * qty, 2)
            turnover = (pos["entry_price"] + final_price) * qty
            commission = round(turnover * commission_rate, 2)
            total_commission += commission

            trades.append({
                "type": "SELL-END",
                "time": df.index[-1],
                "price": final_price,
                "details": pos,
                "quantity": qty,
                "pnl": pnl,
                "commission": commission
            })
            capital += final_price * qty
        positions = []

    metrics = calculate_metrics(trades, initial_capital)

    return {
        "strategy_name": strategy.get("strategy_name", "Unnamed"),
        "symbol": strategy.get("symbol"),
        "timeframe": strategy.get("timeframe"),
        "starting_capital": initial_capital,
        "final_capital": capital,
        **metrics,
        "trades": trades,
        "add_to_position_summary": {
            "capital_pool": add_capital_pool,
            "capital_used": add_capital_pool - remaining_add_capital,
            "triggered": atp_triggered,
            "executed": atp_executed,
            "skipped": atp_skipped_reasons
        }
    }
