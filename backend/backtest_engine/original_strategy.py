from __future__ import annotations

import sys
from importlib import import_module

from core.settings import ORIGINAL_SRC_ROOT


if str(ORIGINAL_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_SRC_ROOT))


_strategy_module = import_module("strategy.sunrise_ogle_xauusd")

SunriseOgle = _strategy_module.SunriseOgle

# Script-level defaults preserved from the original project
DATA_FILENAME = _strategy_module.DATA_FILENAME
FROMDATE = _strategy_module.FROMDATE
TODATE = _strategy_module.TODATE
STARTING_CASH = _strategy_module.STARTING_CASH
QUICK_TEST = _strategy_module.QUICK_TEST
LIMIT_BARS = _strategy_module.LIMIT_BARS
ENABLE_PLOT = _strategy_module.ENABLE_PLOT
ENABLE_FOREX_CALC = _strategy_module.ENABLE_FOREX_CALC
FOREX_INSTRUMENT = _strategy_module.FOREX_INSTRUMENT
TEST_FOREX_MODE = _strategy_module.TEST_FOREX_MODE
RUN_DUAL_CEREBRO = _strategy_module.RUN_DUAL_CEREBRO


def get_strategy_default_params() -> dict:
    return dict(SunriseOgle.params._getitems())
