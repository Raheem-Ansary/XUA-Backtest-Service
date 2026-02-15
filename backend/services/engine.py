from __future__ import annotations

import inspect

from .. import strategies


def get_available_strategies() -> dict[str, type]:
    strategy_classes: dict[str, type] = {}
    for name, obj in inspect.getmembers(strategies):
        if inspect.isclass(obj):
            strategy_classes[name] = obj
    return strategy_classes

