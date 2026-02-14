from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BacktestConfig:
    symbol: str
    timeframe: str
    start_date: str | None
    end_date: str | None
    data_file: str | None
    initial_cash: float
    limit_bars: int
    run_dual_cerebro: bool
    use_forex_position_calc: bool
    strategy_params: dict[str, Any] = field(default_factory=dict)


@dataclass
class BacktestResult:
    backtest_id: str
    symbol: str
    timeframe: str
    start_date: str | None
    end_date: str | None
    initial_cash: float
    final_value: float
    net_profit: float
    total_return_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float | None
    total_trades: int
    win_rate_pct: float
    trade_list: list[dict[str, Any]]
    equity_curve: list[dict[str, Any]]
    strategy_params: dict[str, Any]


@dataclass
class ExecutionArtifacts:
    final_value: float
    analyzers: dict[str, Any]
    strategy_instance: Any
    used_config: BacktestConfig
    used_params: dict[str, Any]


def datetime_to_iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None
