from __future__ import annotations

from .. import strategies


def get_available_strategies() -> dict[str, type]:
    return strategies.get_available_strategies()
