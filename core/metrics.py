from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "channel",
    "campaign",
    "region",
    "device",
    "sessions",
    "orders",
    "revenue",
    "cost",
    "users",
    "new_users",
]


def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    if "date" in work.columns:
        work["date"] = pd.to_datetime(work["date"], errors="coerce")
    for col in REQUIRED_COLUMNS:
        if col not in work.columns:
            work[col] = 0 if col not in {"channel", "campaign", "region", "device"} else "unknown"
    for col in ["sessions", "orders", "revenue", "cost", "users", "new_users"]:
        work[col] = pd.to_numeric(work[col], errors="coerce").fillna(0)
    return work[REQUIRED_COLUMNS]


def add_marketing_metrics(df: pd.DataFrame) -> pd.DataFrame:
    work = ensure_schema(df)
    work["conversion"] = np.where(work["sessions"] > 0, work["orders"] / work["sessions"], 0)
    work["cac"] = np.where(work["orders"] > 0, work["cost"] / work["orders"], 0)
    work["aov"] = np.where(work["orders"] > 0, work["revenue"] / work["orders"], 0)
    work["romi"] = np.where(work["cost"] > 0, (work["revenue"] - work["cost"]) / work["cost"], 0)
    work["ltv"] = work["aov"] * 3
    work["retention"] = np.where(work["users"] > 0, 1 - work["new_users"] / work["users"], 0).clip(0, 1)
    return work


def aggregate_period(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    work = add_marketing_metrics(df)
    agg = work.groupby(by, dropna=False).agg(
        sessions=("sessions", "sum"),
        orders=("orders", "sum"),
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        users=("users", "sum"),
        new_users=("new_users", "sum"),
    ).reset_index()
    return add_marketing_metrics(agg)


def compare_periods(df: pd.DataFrame, start_a, end_a, start_b, end_b) -> pd.DataFrame:
    work = add_marketing_metrics(df)
    a = work[(work["date"] >= start_a) & (work["date"] <= end_a)]
    b = work[(work["date"] >= start_b) & (work["date"] <= end_b)]
    metric_cols = ["sessions", "orders", "revenue", "cost", "conversion", "romi"]
    summary = []
    for metric in metric_cols:
        va = a[metric].sum() if metric in ["sessions", "orders", "revenue", "cost"] else a[metric].mean()
        vb = b[metric].sum() if metric in ["sessions", "orders", "revenue", "cost"] else b[metric].mean()
        change = ((va - vb) / vb * 100) if vb else 0
        summary.append({"Метрика": metric, "Текущий период": va, "Базовый период": vb, "Изменение %": change})
    return pd.DataFrame(summary)


def build_cohort(df: pd.DataFrame) -> pd.DataFrame:
    work = ensure_schema(df)
    work["order_month"] = work["date"].dt.to_period("M").dt.to_timestamp()
    first_month = work.groupby("campaign")["order_month"].transform("min")
    work["cohort"] = first_month
    work["period"] = ((work["order_month"].dt.year - work["cohort"].dt.year) * 12 + (work["order_month"].dt.month - work["cohort"].dt.month))
    pivot = work.pivot_table(index="cohort", columns="period", values="orders", aggfunc="sum").fillna(0)
    base = pivot.iloc[:, 0].replace(0, np.nan)
    retention = pivot.divide(base, axis=0).fillna(0)
    retention.index = retention.index.astype(str)
    return retention
