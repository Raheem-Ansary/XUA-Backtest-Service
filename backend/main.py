from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.backtests import router as backtest_router
from core.settings import DEFAULT_ALLOWED_ORIGINS


app = FastAPI(title="XAUUSD Backtest API", version="1.0.0")

origins_env = os.getenv("BACKEND_CORS_ORIGINS", "")
if origins_env.strip():
    allow_origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
else:
    allow_origins = DEFAULT_ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(backtest_router)
