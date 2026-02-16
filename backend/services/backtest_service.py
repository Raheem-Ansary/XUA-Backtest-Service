from __future__ import annotations

import uuid
from datetime import datetime

from ..backtest_engine.original_strategy import get_default_dates
from ..backtest_engine.result_serializer import build_backtest_result
from ..backtest_engine.runner import default_backtest_config_kwargs, run_backtest
from ..database.repository import BacktestRepository
from ..models.backtest import BacktestConfig
from ..schemas.backtest import BacktestRequest


class BacktestService:
    def __init__(self, repository: BacktestRepository) -> None:
        self.repository = repository

    def create_job(self, payload: BacktestRequest) -> str:
        job_id = str(uuid.uuid4())
        self.repository.create_job(job_id, payload.model_dump())
        return job_id

    def build_config(self, payload: BacktestRequest) -> BacktestConfig:
        defaults = default_backtest_config_kwargs()
        from_date, to_date = get_default_dates()

        # allow top-level extras to override strategy params dynamically
        payload_dict = payload.model_dump()
        core_fields = {
            "symbol",
            "timeframe",
            "start_date",
            "end_date",
            "data_file",
            "initial_cash",
            "risk_percent",
            "atr_multiplier",
            "pullback_window",
            "limit_bars",
            "run_dual_cerebro",
            "use_forex_position_calc",
            "strategy_params",
        }
        extra_params = {k: v for k, v in payload_dict.items() if k not in core_fields}

        strategy_params = dict(payload.strategy_params)
        strategy_params.update(extra_params)

        if payload.risk_percent is not None:
            strategy_params["risk_percent"] = payload.risk_percent
        if payload.atr_multiplier is not None:
            strategy_params["atr_multiplier"] = payload.atr_multiplier
        if payload.pullback_window is not None:
            strategy_params["pullback_window"] = payload.pullback_window

        return BacktestConfig(
            symbol=payload.symbol,
            timeframe=payload.timeframe,
            start_date=payload.start_date or from_date,
            end_date=payload.end_date or to_date,
            data_file=payload.data_file,
            initial_cash=payload.initial_cash or defaults["initial_cash"],
            limit_bars=payload.limit_bars if payload.limit_bars is not None else defaults["limit_bars"],
            run_dual_cerebro=(
                payload.run_dual_cerebro
                if payload.run_dual_cerebro is not None
                else defaults["run_dual_cerebro"]
            ),
            use_forex_position_calc=(
                payload.use_forex_position_calc
                if payload.use_forex_position_calc is not None
                else defaults["use_forex_position_calc"]
            ),
            strategy_params=strategy_params,
        )

    def execute_job(self, job_id: str, payload: BacktestRequest) -> None:
        self.repository.update_status(job_id, "running")
        try:
            config = self.build_config(payload)
            artifacts = run_backtest(config)
            result = build_backtest_result(job_id, artifacts)
            self.repository.save_result(job_id, {
                "backtest_id": result.backtest_id,
                "symbol": result.symbol,
                "timeframe": result.timeframe,
                "start_date": result.start_date,
                "end_date": result.end_date,
                "initial_cash": result.initial_cash,
                "final_value": result.final_value,
                "net_profit": result.net_profit,
                "total_return_pct": result.total_return_pct,
                "max_drawdown_pct": result.max_drawdown_pct,
                "sharpe_ratio": result.sharpe_ratio,
                "total_trades": result.total_trades,
                "win_rate_pct": result.win_rate_pct,
                "trade_list": result.trade_list,
                "equity_curve": result.equity_curve,
                "strategy_params": result.strategy_params,
                "completed_at": datetime.utcnow().isoformat(),
            })
        except Exception as exc:
            self.repository.update_status(job_id, "failed", error=str(exc))

    def get_job(self, job_id: str) -> dict | None:
        return self.repository.get_job(job_id)
