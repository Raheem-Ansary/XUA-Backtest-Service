from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from ..core.settings import DATABASE_PATH


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BacktestRepository:
    def __init__(self, db_path: Path = DATABASE_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS backtests (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    result_json TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_job(self, job_id: str, request_data: dict) -> None:
        now = utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO backtests (id, status, request_json, result_json, error, created_at, updated_at)
                VALUES (?, ?, ?, NULL, NULL, ?, ?)
                """,
                (job_id, "queued", json.dumps(request_data), now, now),
            )
            conn.commit()

    def update_status(self, job_id: str, status: str, error: str | None = None) -> None:
        now = utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                "UPDATE backtests SET status = ?, error = ?, updated_at = ? WHERE id = ?",
                (status, error, now, job_id),
            )
            conn.commit()

    def save_result(self, job_id: str, result_data: dict) -> None:
        now = utc_now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE backtests
                SET status = ?, result_json = ?, error = NULL, updated_at = ?
                WHERE id = ?
                """,
                ("completed", json.dumps(result_data), now, job_id),
            )
            conn.commit()

    def get_job(self, job_id: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM backtests WHERE id = ?", (job_id,)).fetchone()

        if row is None:
            return None

        return {
            "id": row["id"],
            "status": row["status"],
            "request": json.loads(row["request_json"]) if row["request_json"] else None,
            "result": json.loads(row["result_json"]) if row["result_json"] else None,
            "error": row["error"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
