from __future__ import annotations

from datetime import datetime
from pathlib import Path

import backtrader as bt

from core.settings import DEFAULT_DATA_FILE, ORIGINAL_DATA_ROOT


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def resolve_data_file(data_file: str | None) -> Path:
    if not data_file:
        return DEFAULT_DATA_FILE

    candidate = Path(data_file)
    if candidate.is_absolute():
        return candidate

    in_original_data = ORIGINAL_DATA_ROOT / data_file
    if in_original_data.exists():
        return in_original_data

    return candidate


def load_feed(data_file: str | None, start_date: str | None, end_date: str | None) -> bt.feeds.GenericCSVData:
    resolved = resolve_data_file(data_file)
    if not resolved.exists():
        raise FileNotFoundError(f"Data file not found: {resolved}")

    feed_kwargs = {
        "dataname": str(resolved),
        "dtformat": "%Y%m%d",
        "tmformat": "%H:%M:%S",
        "datetime": 0,
        "time": 1,
        "open": 2,
        "high": 3,
        "low": 4,
        "close": 5,
        "volume": 6,
        "timeframe": bt.TimeFrame.Minutes,
        "compression": 5,
    }

    fromdate = parse_date(start_date)
    todate = parse_date(end_date)
    if fromdate:
        feed_kwargs["fromdate"] = fromdate
    if todate:
        feed_kwargs["todate"] = todate

    return bt.feeds.GenericCSVData(**feed_kwargs)
