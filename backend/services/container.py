from __future__ import annotations

from ..database.repository import BacktestRepository
from .backtest_service import BacktestService


_repository: BacktestRepository | None = None
_service: BacktestService | None = None


def get_backtest_service() -> BacktestService:
    global _repository, _service
    if _repository is None:
        _repository = BacktestRepository()
    if _service is None:
        _service = BacktestService(_repository)
    return _service
