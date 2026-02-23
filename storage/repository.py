from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime
from hashlib import md5

import pandas as pd
from sqlalchemy import text

from core.config import AppConfig
from core.metrics import ensure_schema
from storage.db import get_engine


def _file_hash(data: bytes) -> str:
    return md5(data).hexdigest()


def upsert_dataframe(config: AppConfig, df: pd.DataFrame, source_name: str, raw_bytes: bytes | None = None) -> str:
    engine = get_engine(config)
    marker = _file_hash(raw_bytes) if raw_bytes else source_name

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM marketing_raw WHERE source_file=:source_file"), {"source_file": marker})

    data = df.copy()
    data["source_file"] = marker
    data["updated_at"] = datetime.now().isoformat()
    data.to_sql("marketing_raw", engine, if_exists="append", index=False)
    return marker


def append_manual_row(config: AppConfig, row: dict) -> str:
    df = ensure_schema(pd.DataFrame([row]))
    return upsert_dataframe(config, df, source_name=f"manual_{datetime.now().isoformat()}")


def import_sqlite_database(config: AppConfig, db_bytes: bytes, table_name: str = "marketing_raw") -> int:
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        tmp.write(db_bytes)
        tmp.flush()
        with sqlite3.connect(tmp.name) as conn:
            source_df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    clean = ensure_schema(source_df)
    upsert_dataframe(config, clean, source_name=f"sqlite_import_{datetime.now().isoformat()}", raw_bytes=db_bytes)
    return len(clean)


def fetch_data(config: AppConfig) -> pd.DataFrame:
    engine = get_engine(config)
    return pd.read_sql("SELECT * FROM marketing_raw", engine)


def save_report(config: AppConfig, period_start: str, period_end: str, report_html: str) -> None:
    engine = get_engine(config)
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO reports_history(created_at, period_start, period_end, report_html) VALUES(:created_at, :ps, :pe, :rh)"
            ),
            {"created_at": datetime.now().isoformat(), "ps": period_start, "pe": period_end, "rh": report_html},
        )


def load_reports(config: AppConfig) -> pd.DataFrame:
    engine = get_engine(config)
    return pd.read_sql("SELECT * FROM reports_history ORDER BY id DESC", engine)
