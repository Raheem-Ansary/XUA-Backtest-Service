from __future__ import annotations

import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import DEFAULT_ALLOWED_ORIGINS
from .routers.backtests import router as backtest_router


app = FastAPI(title="XAUUSD Backtest API", version="1.0.0")
print("PYTHONPATH:", sys.path)

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
