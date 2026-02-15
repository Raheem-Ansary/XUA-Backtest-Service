from __future__ import annotations

import asyncio
from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..backtest_engine.original_strategy import get_strategy_default_params
from ..schemas.backtest import BacktestRequest, BacktestResponse
from ..services.container import get_backtest_service


router = APIRouter(prefix="/api/backtest", tags=["backtest"])


@router.get("/parameters")
def get_parameters() -> dict:
    return {"strategy_params": get_strategy_default_params()}


@router.post("/run", response_model=BacktestResponse)
async def run_backtest(payload: BacktestRequest) -> BacktestResponse:
    service = get_backtest_service()
    job_id = service.create_job(payload)

    async def _run() -> None:
        await asyncio.to_thread(service.execute_job, job_id, payload)

    asyncio.create_task(_run())

    now = datetime.utcnow()
    return BacktestResponse(
        id=job_id,
        status="queued",
        created_at=now,
        updated_at=now,
        result=None,
        error=None,
    )


@router.get("/{backtest_id}", response_model=BacktestResponse)
def get_backtest(backtest_id: str) -> BacktestResponse:
    service = get_backtest_service()
    job = service.get_job(backtest_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Backtest not found")

    return BacktestResponse(
        id=job["id"],
        status=job["status"],
        created_at=datetime.fromisoformat(job["created_at"]),
        updated_at=datetime.fromisoformat(job["updated_at"]),
        error=job["error"],
        result=job["result"],
    )


@router.get("/{backtest_id}/equity-curve")
def get_equity_curve(backtest_id: str) -> dict:
    service = get_backtest_service()
    job = service.get_job(backtest_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if job["status"] != "completed" or not job.get("result"):
        return {"id": backtest_id, "status": job["status"], "equity_curve": []}

    return {
        "id": backtest_id,
        "status": job["status"],
        "equity_curve": job["result"].get("equity_curve", []),
    }

