from __future__ import annotations

import math
from datetime import datetime
from typing import Any

from ..models.backtest import BacktestResult, ExecutionArtifacts


def _normalize_drawdown(drawdown_raw: float | int | None) -> float:
    if drawdown_raw is None:
        return 0.0
    value = abs(float(drawdown_raw))
    if value <= 1.0:
        value *= 100.0
    return min(value, 99.9)


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if math.isfinite(numeric):
        return numeric
    return None


def _extract_trade_list(strategy_instance: Any) -> list[dict[str, Any]]:
    trade_reports = getattr(strategy_instance, "trade_reports", []) or []
    trades: list[dict[str, Any]] = []

    for trade in trade_reports:
        entry_time = trade.get("entry_time")
        exit_time = trade.get("exit_time")
        trades.append(
            {
                "entry_time": entry_time.isoformat() if isinstance(entry_time, datetime) else None,
                "exit_time": exit_time.isoformat() if isinstance(exit_time, datetime) else None,
                "direction": trade.get("direction"),
                "entry_price": trade.get("entry_price"),
                "exit_price": trade.get("exit_price"),
                "size": trade.get("size"),
                "pnl": trade.get("pnl"),
                "exit_reason": trade.get("exit_reason"),
            }
        )

    return trades


def _extract_equity_curve(strategy_instance: Any) -> list[dict[str, Any]]:
    timestamps = getattr(strategy_instance, "_timestamps", []) or []
    values = getattr(strategy_instance, "_portfolio_values", []) or []

    points: list[dict[str, Any]] = []
    for ts, value in zip(timestamps, values):
        if not isinstance(ts, datetime):
            continue
        points.append({"timestamp": ts.isoformat(), "value": float(value)})

    return points


def build_backtest_result(backtest_id: str, artifacts: ExecutionArtifacts) -> BacktestResult:
    trade_analyzer = artifacts.analyzers.get("trades", {})
    drawdown_analyzer = artifacts.analyzers.get("drawdown", {})
    sharpe_analyzer = artifacts.analyzers.get("sharpe", {})

    total_trades = int(trade_analyzer.get("total", {}).get("total", 0) or 0)
    won_trades = int(trade_analyzer.get("won", {}).get("total", 0) or 0)

    sharpe_value = _safe_float(sharpe_analyzer.get("sharperatio"))
    max_drawdown_pct = _normalize_drawdown(drawdown_analyzer.get("max", {}).get("drawdown", 0.0))

    initial_cash = artifacts.used_config.initial_cash
    final_value = float(artifacts.final_value)
    net_profit = final_value - initial_cash
    total_return_pct = (net_profit / initial_cash) * 100 if initial_cash else 0.0
    win_rate_pct = (won_trades / total_trades) * 100 if total_trades else 0.0

    return BacktestResult(
        backtest_id=backtest_id,
        symbol=artifacts.used_config.symbol,
        timeframe=artifacts.used_config.timeframe,
        start_date=artifacts.used_config.start_date,
        end_date=artifacts.used_config.end_date,
        initial_cash=initial_cash,
        final_value=final_value,
        net_profit=net_profit,
        total_return_pct=total_return_pct,
        max_drawdown_pct=max_drawdown_pct,
        sharpe_ratio=sharpe_value,
        total_trades=total_trades,
        win_rate_pct=win_rate_pct,
        trade_list=_extract_trade_list(artifacts.strategy_instance),
        equity_curve=_extract_equity_curve(artifacts.strategy_instance),
        strategy_params=artifacts.used_params,
    )
