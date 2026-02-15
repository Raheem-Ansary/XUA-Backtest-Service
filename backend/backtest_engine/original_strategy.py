from __future__ import annotations

from .. import strategies
from ..services.engine import get_available_strategies


SunriseOgle = get_available_strategies()["SunriseOgle"]

# Script-level defaults preserved from the original project
DATA_FILENAME = strategies.DATA_FILENAME
FROMDATE = strategies.FROMDATE
TODATE = strategies.TODATE
STARTING_CASH = strategies.STARTING_CASH
QUICK_TEST = strategies.QUICK_TEST
LIMIT_BARS = strategies.LIMIT_BARS
ENABLE_PLOT = strategies.ENABLE_PLOT
ENABLE_FOREX_CALC = strategies.ENABLE_FOREX_CALC
FOREX_INSTRUMENT = strategies.FOREX_INSTRUMENT
TEST_FOREX_MODE = strategies.TEST_FOREX_MODE
RUN_DUAL_CEREBRO = strategies.RUN_DUAL_CEREBRO


def get_strategy_default_params() -> dict:
    return dict(SunriseOgle.params._getitems())
