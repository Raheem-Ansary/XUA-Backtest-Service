from __future__ import annotations

from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_ROOT.parent
ORIGINAL_PROJECT_ROOT = PROJECT_ROOT / "backtrader-pullback-window-xauusd"
ORIGINAL_SRC_ROOT = ORIGINAL_PROJECT_ROOT / "src"
ORIGINAL_DATA_ROOT = ORIGINAL_PROJECT_ROOT / "data"

DATABASE_PATH = BACKEND_ROOT / "database" / "backtests.db"
DEFAULT_DATA_FILE = ORIGINAL_DATA_ROOT / "XAUUSD_5m_5Yea.csv"

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
