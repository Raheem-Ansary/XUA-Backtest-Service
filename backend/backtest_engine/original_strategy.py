from __future__ import annotations

from .. import strategies


def get_sunrise_ogle_class():
    return strategies.get_strategy_class("SunriseOgle")


def get_strategy_runtime_config() -> dict:
    return {
        "DATA_FILENAME": strategies.get_strategy_constant("DATA_FILENAME"),
        "FROMDATE": strategies.get_strategy_constant("FROMDATE"),
        "TODATE": strategies.get_strategy_constant("TODATE"),
        "STARTING_CASH": strategies.get_strategy_constant("STARTING_CASH"),
        "QUICK_TEST": strategies.get_strategy_constant("QUICK_TEST"),
        "LIMIT_BARS": strategies.get_strategy_constant("LIMIT_BARS"),
        "ENABLE_PLOT": strategies.get_strategy_constant("ENABLE_PLOT"),
        "ENABLE_FOREX_CALC": strategies.get_strategy_constant("ENABLE_FOREX_CALC"),
        "FOREX_INSTRUMENT": strategies.get_strategy_constant("FOREX_INSTRUMENT"),
        "TEST_FOREX_MODE": strategies.get_strategy_constant("TEST_FOREX_MODE"),
        "RUN_DUAL_CEREBRO": strategies.get_strategy_constant("RUN_DUAL_CEREBRO"),
    }


def get_strategy_default_params() -> dict:
    strategy_class = get_sunrise_ogle_class()
    return dict(strategy_class.params._getitems())


def get_default_dates() -> tuple[str | None, str | None]:
    config = get_strategy_runtime_config()
    return config["FROMDATE"], config["TODATE"]
