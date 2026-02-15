# XAU Backtest Web Platform

Production-style full-stack backtesting platform for the XAUUSD strategy.

This project contains:
- Original Backtrader strategy project: `backtrader-pullback-window-xauusd`
- FastAPI backend service wrapper: `backend`
- Next.js frontend dashboard: `frontend`

The backend runs the original `SunriseOgle` strategy class directly and exposes async REST APIs for running and retrieving backtests.

## Table of Contents

1. Overview
2. Architecture
3. Project Structure
4. Prerequisites
5. Backend Setup
6. Frontend Setup
7. Run Full Stack Locally
8. API Reference
9. Backtest Request Parameters
10. Data Source
11. Troubleshooting
12. License

## 1. Overview

The platform provides:
- Backtest execution via API (`POST /api/backtest/run`)
- Async/background execution (server remains responsive)
- Stored job status/results in SQLite
- Frontend form to configure parameters dynamically
- Dashboard with:
  - Performance summary cards
  - Equity curve chart
  - Trade list table

## 2. Architecture

- Strategy engine: Backtrader (original strategy logic preserved)
- API layer: FastAPI
- Persistence: SQLite (`backend/database/backtests.db`)
- Frontend: Next.js App Router

Execution flow:
1. Frontend submits config to backend
2. Backend creates backtest job ID and returns immediately
3. Backend runs backtest in background thread
4. Frontend polls job endpoint until completion
5. Frontend renders result metrics/equity/trades

## 3. Project Structure

```text
xau-back-test-web/
├── backtrader-pullback-window-xauusd/
│   ├── src/strategy/sunrise_ogle_xauusd.py
│   └── data/XAUUSD_5m_5Yea.csv
├── backend/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── core/
│   ├── backtest_engine/
│   └── database/
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/api.js
└── README.md
```

## 4. Prerequisites

- Python 3.10+
- Node.js 18+
- npm (or yarn)

## 5. Backend Setup

From repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Optional CORS override:

```bash
export BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

Health check:

```bash
curl http://localhost:8000/health
```

## 6. Frontend Setup

From repository root:

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run frontend:

```bash
npm run dev
```

Open:
- `http://localhost:3000`

## 7. Run Full Stack Locally

1. Start backend on port `8000`
2. Start frontend on port `3000`
3. Go to `/run-backtest`
4. Configure parameters
5. Click `Run Backtest`
6. Watch status and results

## 8. API Reference

### `POST /api/backtest/run`

Create and start a new backtest job.

Request body example:

```json
{
  "symbol": "XAUUSD",
  "timeframe": "5m",
  "start_date": "2020-07-10",
  "end_date": "2025-07-25",
  "initial_cash": 100000,
  "strategy_params": {
    "risk_percent": 0.01,
    "long_entry_window_periods": 7,
    "short_entry_window_periods": 7
  }
}
```

Response example:

```json
{
  "id": "0f2b9ec5-2f5f-4c83-a456-52f8a842a1f2",
  "status": "queued",
  "created_at": "2026-02-14T12:00:00.000000",
  "updated_at": "2026-02-14T12:00:00.000000",
  "error": null,
  "result": null
}
```

### `GET /api/backtest/{id}`

Get job status and completed result payload.

Statuses:
- `queued`
- `running`
- `completed`
- `failed`

### `GET /api/backtest/{id}/equity-curve`

Get only equity curve data for a completed job.

### `GET /api/backtest/parameters`

Returns all strategy default parameters discovered from original strategy class.

## 9. Backtest Request Parameters

Core fields:
- `symbol`
- `timeframe`
- `start_date`
- `end_date`
- `initial_cash`
- `data_file` (optional)
- `limit_bars` (optional)
- `run_dual_cerebro` (optional)
- `use_forex_position_calc` (optional)
- `strategy_params` (dictionary with strategy overrides)

Result includes:
- `total_return_pct`
- `net_profit`
- `max_drawdown_pct`
- `sharpe_ratio`
- `total_trades`
- `win_rate_pct`
- `equity_curve`
- `trade_list`

## 10. Data Source

Default file:
- `backtrader-pullback-window-xauusd/data/XAUUSD_5m_5Yea.csv`

You can override by sending `data_file` in request payload.

## 11. Troubleshooting

Backend fails with `ModuleNotFoundError`:
- Ensure backend venv is activated
- Reinstall dependencies with `pip install -r requirements.txt`

Frontend cannot call backend:
- Confirm `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Confirm backend runs on matching host/port
- Check CORS origins in backend config

Backtest job stuck:
- Check backend logs for strategy/data errors
- Verify CSV path and format

## 12. License

This project is licensed under the MIT License.
See `LICENSE`.
