from __future__ import annotations

import logging
from importlib.util import module_from_spec, spec_from_file_location
import inspect
from pathlib import Path
from types import ModuleType

logger = logging.getLogger(__name__)


def _repo_root() -> Path:
    # backend/strategies.py -> backend -> repo root
    return Path(__file__).resolve().parents[1]


def _strategy_directories() -> list[Path]:
    src_root = _repo_root() / "backtrader-pullback-window-xauusd" / "src"
    return [src_root / "strategy", src_root / "strategies"]


def _strategy_file_candidates() -> list[Path]:
    # Keep compatible with historical Windows/Linux naming differences.
    names = [
        "sunrise_ogle_xauusd.py",
        "Sunrise_ogle_xauusd.py",
        "Sunrise_Ogle_XAUUSD.py",
    ]
    return [directory / name for directory in _strategy_directories() for name in names]


def _list_strategy_files() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for directory in _strategy_directories():
        if directory.exists():
            found[str(directory)] = sorted(path.name for path in directory.glob("*.py"))
        else:
            found[str(directory)] = []
    return found


_LOADED_MODULE: ModuleType | None = None


def load_strategy_module() -> ModuleType:
    global _LOADED_MODULE
    if _LOADED_MODULE is not None:
        return _LOADED_MODULE

    repo_root = _repo_root()
    strategy_dirs = _strategy_directories()
    candidates = _strategy_file_candidates()

    logger.info("Strategy repo_root=%s", repo_root)
    logger.info("Strategy directories=%s", [str(path) for path in strategy_dirs])

    strategy_file = next((path for path in candidates if path.exists()), None)
    if strategy_file is None:
        available = _list_strategy_files()
        logger.error("Strategy file candidates=%s", [str(path) for path in candidates])
        logger.error("Available strategy .py files=%s", available)
        raise FileNotFoundError(
            "Strategy file not found. "
            f"repo_root={repo_root}; "
            f"strategy_dirs={[str(path) for path in strategy_dirs]}; "
            f"candidates={[str(path) for path in candidates]}; "
            f"available={available}"
        )

    logger.info("Using strategy file=%s", strategy_file)
    spec = spec_from_file_location("backend_original_sunrise_ogle_xauusd", strategy_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load strategy module from {strategy_file}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    _LOADED_MODULE = module
    return module


def get_strategy_class(name: str) -> type:
    module = load_strategy_module()
    try:
        value = getattr(module, name)
    except AttributeError as exc:
        raise KeyError(f"Strategy class not found: {name}") from exc
    if not inspect.isclass(value):
        raise TypeError(f"Attribute {name} exists but is not a class")
    return value


def get_strategy_constant(name: str):
    module = load_strategy_module()
    try:
        return getattr(module, name)
    except AttributeError as exc:
        raise KeyError(f"Strategy constant not found: {name}") from exc


def get_available_strategies() -> dict[str, type]:
    module = load_strategy_module()
    strategy_classes: dict[str, type] = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and getattr(obj, "__module__", "") == module.__name__:
            strategy_classes[name] = obj
    return strategy_classes
