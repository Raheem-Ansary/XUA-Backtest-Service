# Backend Service

FastAPI wrapper around the original Backtrader XAUUSD strategy.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `POST /api/backtest/run` submit async job
- `GET /api/backtest/{id}` get job status/result
- `GET /api/backtest/{id}/equity-curve` get equity series
- `GET /api/backtest/parameters` list all strategy parameters

## Storage

SQLite DB file: `database/backtests.db`
