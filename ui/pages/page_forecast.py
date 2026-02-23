from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.config import AppConfig
from core.forecast import forecast_series
from core.insights import detect_anomalies
from core.metrics import add_marketing_metrics
from storage.repository import fetch_data


def render(config: AppConfig) -> None:
    st.header("Прогноз")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return
    df["date"] = pd.to_datetime(df["date"])
    df = add_marketing_metrics(df)

    metric = st.selectbox("Метрика", ["revenue", "orders", "sessions", "cost"])
    horizon = st.selectbox("Горизонт", [7, 30, 90], index=1)
    fc = forecast_series(df, metric, horizon)
    st.plotly_chart(px.line(fc, x="date", y=["value", "prediction"], title=f"Прогноз {metric} на {horizon} дней"), use_container_width=True)

    anomalies = detect_anomalies(df, metric="conversion")
    st.subheader("Аномалии конверсии")
    st.dataframe(anomalies, use_container_width=True)
