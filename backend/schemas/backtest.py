from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EquityPoint(BaseModel):
    timestamp: datetime
    value: float


class TradeModel(BaseModel):
    entry_time: datetime | None = None
    exit_time: datetime | None = None
    direction: str | None = None
    entry_price: float | None = None
    exit_price: float | None = None
    size: float | None = None
    pnl: float | None = None
    exit_reason: str | None = None


class BacktestRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    symbol: str = "XAUUSD"
    timeframe: str = "5m"
    start_date: str | None = None
    end_date: str | None = None
    data_file: str | None = None
    initial_cash: float | None = None
    risk_percent: float | None = None
    atr_multiplier: float | None = None
    pullback_window: int | None = None
    limit_bars: int | None = None
    run_dual_cerebro: bool | None = None
    use_forex_position_calc: bool | None = None
    strategy_params: dict[str, Any] = Field(default_factory=dict)


class BacktestResponse(BaseModel):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    error: str | None = None
    result: dict[str, Any] | None = None


class BacktestResultPayload(BaseModel):
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
    trade_list: list[TradeModel]
    equity_curve: list[EquityPoint]
    strategy_params: dict[str, Any]
