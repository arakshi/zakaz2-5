from __future__ import annotations

import pandas as pd


def detect_anomalies(df: pd.DataFrame, metric: str = "conversion", window: int = 7) -> pd.DataFrame:
    daily = df.groupby("date", as_index=False)[metric].mean().sort_values("date")
    daily["ma"] = daily[metric].rolling(window=window, min_periods=3).mean()
    daily["std"] = daily[metric].rolling(window=window, min_periods=3).std().fillna(0)
    daily["is_anomaly"] = (daily[metric] < daily["ma"] - 2 * daily["std"]) | (daily[metric] > daily["ma"] + 2 * daily["std"])
    return daily[daily["is_anomaly"]].copy()


def budget_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    ch = df.groupby("channel", as_index=False).agg(revenue=("revenue", "sum"), cost=("cost", "sum"), orders=("orders", "sum"))
    ch["romi"] = (ch["revenue"] - ch["cost"]) / ch["cost"].replace(0, 1)
    ch["share"] = ch["cost"] / ch["cost"].sum() if ch["cost"].sum() else 0
    median_romi = ch["romi"].median() if not ch.empty else 0
    ch["recommendation"] = ch["romi"].apply(
        lambda x: "Увеличить бюджет на 10-15%" if x > median_romi else "Оптимизировать креативы и снизить бюджет на 5-10%"
    )
    return ch.sort_values("romi", ascending=False)


def period_summary_text(period_comparison: pd.DataFrame) -> str:
    lines = []
    for _, row in period_comparison.iterrows():
        trend = "выросла" if row["Изменение %"] >= 0 else "снизилась"
        lines.append(f"Метрика {row['Метрика']} {trend} на {abs(row['Изменение %']):.1f}%.")
    return " ".join(lines)
