from __future__ import annotations

from collections.abc import Callable

import backtrader as bt

from .data_loader import load_feed
from .original_strategy import (
    get_strategy_runtime_config,
    get_sunrise_ogle_class,
    get_strategy_default_params,
)
from ..models.backtest import BacktestConfig, ExecutionArtifacts


def _build_strategy_kwargs(config: BacktestConfig) -> dict:
    strategy_config = get_strategy_runtime_config()
    params = get_strategy_default_params()
    params.update(config.strategy_params)

    # Convenience aliases requested by API payload
    if "risk_percent" in config.strategy_params:
        params["risk_percent"] = config.strategy_params["risk_percent"]
    if "atr_multiplier" in config.strategy_params:
        params["long_atr_sl_multiplier"] = config.strategy_params["atr_multiplier"]
        params["short_atr_sl_multiplier"] = config.strategy_params["atr_multiplier"]
    if "pullback_window" in config.strategy_params:
        params["long_entry_window_periods"] = config.strategy_params["pullback_window"]
        params["short_entry_window_periods"] = config.strategy_params["pullback_window"]

    params["plot_result"] = False
    params["use_forex_position_calc"] = config.use_forex_position_calc
    params["forex_instrument"] = config.symbol or strategy_config["FOREX_INSTRUMENT"]
    return params


def _add_common_analyzers(cerebro: bt.Cerebro, use_daily_sharpe: bool) -> None:
    if use_daily_sharpe:
        cerebro.addanalyzer(
            bt.analyzers.SharpeRatio,
            _name="sharpe",
            timeframe=bt.TimeFrame.Days,
            riskfreerate=0.0,
        )
    else:
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")

    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")


def _run_single_cerebro(config: BacktestConfig, strategy_kwargs: dict, use_daily_sharpe: bool) -> tuple:
    cerebro = bt.Cerebro(stdstats=False)
    strategy_class = get_sunrise_ogle_class()
    data = load_feed(config.data_file, config.start_date, config.end_date)
    cerebro.adddata(data)
    cerebro.broker.setcash(config.initial_cash)
    cerebro.broker.setcommission(leverage=30.0)
    cerebro.addstrategy(strategy_class, **strategy_kwargs)
    _add_common_analyzers(cerebro, use_daily_sharpe=use_daily_sharpe)

    original_next: Callable | None = None
    limit_bars = config.limit_bars
    if limit_bars > 0:
        original_next = strategy_class.next

        def limited_next(self):
            if len(self.data) >= limit_bars:
                self.env.runstop()
                return
            original_next(self)

        strategy_class.next = limited_next

    try:
        results = cerebro.run()
    finally:
        if original_next is not None:
            strategy_class.next = original_next

    return cerebro, results[0]


def _build_execution_artifacts(
    config: BacktestConfig,
    strategy_instance,
    final_value: float,
    used_params: dict,
) -> ExecutionArtifacts:
    analyzers = {
        "sharpe": strategy_instance.analyzers.getbyname("sharpe").get_analysis(),
        "drawdown": strategy_instance.analyzers.getbyname("drawdown").get_analysis(),
        "trades": strategy_instance.analyzers.getbyname("trades").get_analysis(),
        "returns": strategy_instance.analyzers.getbyname("returns").get_analysis(),
    }
    return ExecutionArtifacts(
        final_value=final_value,
        analyzers=analyzers,
        strategy_instance=strategy_instance,
        used_config=config,
        used_params=used_params,
    )


def run_backtest(config: BacktestConfig) -> ExecutionArtifacts:
    strategy_kwargs = _build_strategy_kwargs(config)
    run_dual = config.run_dual_cerebro

    if run_dual and strategy_kwargs.get("enable_long_trades") and strategy_kwargs.get("enable_short_trades"):
        long_kwargs = dict(strategy_kwargs)
        long_kwargs.update({"long_enabled": True, "short_enabled": False})

        short_kwargs = dict(strategy_kwargs)
        short_kwargs.update({"long_enabled": False, "short_enabled": True})

        cerebro_long, strategy_long = _run_single_cerebro(config, long_kwargs, use_daily_sharpe=True)
        cerebro_short, strategy_short = _run_single_cerebro(config, short_kwargs, use_daily_sharpe=True)

        long_value = cerebro_long.broker.getvalue()
        short_value = cerebro_short.broker.getvalue()
        combined_value = config.initial_cash + ((long_value - config.initial_cash) + (short_value - config.initial_cash))

        # Build a merged proxy object for serializer compatibility
        class CombinedStrategyProxy:
            pass

        proxy = CombinedStrategyProxy()
        proxy.trade_reports = (getattr(strategy_long, "trade_reports", []) or []) + (
            getattr(strategy_short, "trade_reports", []) or []
        )

        long_timestamps = getattr(strategy_long, "_timestamps", []) or []
        short_timestamps = getattr(strategy_short, "_timestamps", []) or []
        long_values = getattr(strategy_long, "_portfolio_values", []) or []
        short_values = getattr(strategy_short, "_portfolio_values", []) or []

        merged_timestamps = long_timestamps[: min(len(long_timestamps), len(short_timestamps))]
        merged_values = []
        for lv, sv in zip(long_values, short_values):
            merged_values.append((lv + sv) - config.initial_cash)
        proxy._timestamps = merged_timestamps[: len(merged_values)]
        proxy._portfolio_values = merged_values

        combined_analyzers = {
            "total": {
                "total": int((strategy_long.analyzers.trades.get_analysis().get("total", {}).get("total", 0) or 0))
                + int((strategy_short.analyzers.trades.get_analysis().get("total", {}).get("total", 0) or 0))
            },
            "won": {
                "total": int((strategy_long.analyzers.trades.get_analysis().get("won", {}).get("total", 0) or 0))
                + int((strategy_short.analyzers.trades.get_analysis().get("won", {}).get("total", 0) or 0))
            },
        }

        drawdown_long = strategy_long.analyzers.drawdown.get_analysis()
        drawdown_short = strategy_short.analyzers.drawdown.get_analysis()
        max_dd_long = drawdown_long.get("max", {}).get("drawdown", 0)
        max_dd_short = drawdown_short.get("max", {}).get("drawdown", 0)

        sharpe_long = strategy_long.analyzers.sharpe.get_analysis().get("sharperatio")
        sharpe_short = strategy_short.analyzers.sharpe.get_analysis().get("sharperatio")
        sharpe_values = [x for x in [sharpe_long, sharpe_short] if isinstance(x, (int, float))]

        return ExecutionArtifacts(
            final_value=combined_value,
            analyzers={
                "trades": combined_analyzers,
                "drawdown": {"max": {"drawdown": max(max_dd_long, max_dd_short)}},
                "sharpe": {"sharperatio": (sum(sharpe_values) / len(sharpe_values)) if sharpe_values else None},
                "returns": {},
            },
            strategy_instance=proxy,
            used_config=config,
            used_params=strategy_kwargs,
        )

    _, strategy = _run_single_cerebro(config, strategy_kwargs, use_daily_sharpe=False)
    return _build_execution_artifacts(
        config=config,
        strategy_instance=strategy,
        final_value=strategy.broker.getvalue(),
        used_params=strategy_kwargs,
    )


def default_backtest_config_kwargs() -> dict:
    strategy_config = get_strategy_runtime_config()
    return {
        "initial_cash": 100000.0,
        "limit_bars": strategy_config["LIMIT_BARS"],
        "run_dual_cerebro": strategy_config["RUN_DUAL_CEREBRO"],
        "use_forex_position_calc": strategy_config["ENABLE_FOREX_CALC"],
    }
