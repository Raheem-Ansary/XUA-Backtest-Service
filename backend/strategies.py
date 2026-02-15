from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
import inspect

from .core.settings import ORIGINAL_SRC_ROOT


_strategy_file = ORIGINAL_SRC_ROOT / "strategy" / "sunrise_ogle_xauusd.py"
_spec = spec_from_file_location("backend_original_sunrise_ogle_xauusd", _strategy_file)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Unable to load strategy module from {_strategy_file}")
_module = module_from_spec(_spec)
_spec.loader.exec_module(_module)

SunriseOgle = _module.SunriseOgle
DATA_FILENAME = _module.DATA_FILENAME
ENABLE_FOREX_CALC = _module.ENABLE_FOREX_CALC
ENABLE_PLOT = _module.ENABLE_PLOT
FOREX_INSTRUMENT = _module.FOREX_INSTRUMENT
FROMDATE = _module.FROMDATE
LIMIT_BARS = _module.LIMIT_BARS
QUICK_TEST = _module.QUICK_TEST
RUN_DUAL_CEREBRO = _module.RUN_DUAL_CEREBRO
STARTING_CASH = _module.STARTING_CASH
TEST_FOREX_MODE = _module.TEST_FOREX_MODE
TODATE = _module.TODATE


def get_available_strategies() -> dict[str, type]:
    strategy_classes: dict[str, type] = {}
    for name, obj in inspect.getmembers(_module):
        if inspect.isclass(obj) and getattr(obj, "__module__", "") == _module.__name__:
            strategy_classes[name] = obj
    return strategy_classes
