from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from core.config import AppConfig

_ENGINE: Engine | None = None


def get_engine(config: AppConfig) -> Engine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_engine(config.db_url, future=True)
    return _ENGINE


def init_db(config: AppConfig) -> None:
    engine = get_engine(config)
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS marketing_raw (
                    date TEXT,
                    channel TEXT,
                    campaign TEXT,
                    region TEXT,
                    device TEXT,
                    sessions REAL,
                    orders REAL,
                    revenue REAL,
                    cost REAL,
                    users REAL,
                    new_users REAL,
                    source_file TEXT,
                    updated_at TEXT
                )
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS reports_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    period_start TEXT,
                    period_end TEXT,
                    report_html TEXT
                )
                """
            )
        )
