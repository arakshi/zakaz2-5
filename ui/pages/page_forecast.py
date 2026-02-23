from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core.config import AppConfig
from core.forecast import FORECAST_METHODS, forecast_series
from core.insights import detect_anomalies
from core.metrics import add_marketing_metrics
from storage.repository import fetch_data


def _plot_forecast(fc: pd.DataFrame, metric: str, horizon: int, method_label: str):
    fig = go.Figure()
    hist = fc[fc["part"] == "history"]
    pred = fc[fc["part"] == "forecast"]

    fig.add_trace(go.Scatter(x=hist["date"], y=hist["value"], mode="lines", name="История"))
    fig.add_trace(go.Scatter(x=pred["date"], y=pred["prediction"], mode="lines+markers", name="Прогноз"))

    fig.add_trace(
        go.Scatter(
            x=pred["date"],
            y=pred["upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=pred["date"],
            y=pred["lower"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(37,99,235,0.15)",
            name="Доверительный диапазон",
        )
    )
    fig.update_layout(title=f"Прогноз {metric} на {horizon} дней ({method_label})")
    return fig


def render(config: AppConfig) -> None:
    st.header("Прогноз")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return

    df["date"] = pd.to_datetime(df["date"])
    df = add_marketing_metrics(df)

    c1, c2, c3 = st.columns(3)
    metric = c1.selectbox("Метрика", ["revenue", "orders", "sessions", "cost"])
    horizon = c2.selectbox("Горизонт", [7, 30, 90], index=1)
    method_label = c3.selectbox("Метод прогноза", list(FORECAST_METHODS.keys()))
    method = FORECAST_METHODS[method_label]

    poly_degree = 2
    ma_window = 7
    if method == "poly":
        poly_degree = st.slider("Степень полинома", min_value=2, max_value=4, value=2)
    if method == "moving_avg":
        ma_window = st.slider("Окно скользящего среднего", min_value=3, max_value=30, value=7)

    fc = forecast_series(df, metric, horizon, method=method, poly_degree=poly_degree, ma_window=ma_window)
    st.plotly_chart(_plot_forecast(fc, metric, horizon, method_label), use_container_width=True)

    st.subheader("Сравнение прогнозов по всем KPI")
    cols = st.columns(4)
    for idx, kpi in enumerate(["revenue", "orders", "sessions", "cost"]):
        mini = forecast_series(df, kpi, horizon, method=method, poly_degree=poly_degree, ma_window=ma_window)
        future_sum = mini[mini["part"] == "forecast"]["prediction"].sum()
        cols[idx].metric(f"{kpi} ({horizon}д)", f"{future_sum:,.1f}")

    anomalies = detect_anomalies(df, metric="conversion")
    st.subheader("Аномалии конверсии")
    st.dataframe(anomalies, use_container_width=True)
