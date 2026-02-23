from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.config import AppConfig
from core.metrics import add_marketing_metrics
from storage.repository import fetch_data
from ui.layout import date_filters


def render(config: AppConfig) -> None:
    st.header("Дашборд")
    df = fetch_data(config)
    if df.empty:
        st.info("Данные отсутствуют. Откройте раздел «Демо» и сгенерируйте данные.")
        return
    df["date"] = pd.to_datetime(df["date"])
    df = add_marketing_metrics(df)

    d1, d2, channels = date_filters(df)
    if d1 and d2:
        df = df[(df["date"].dt.date >= d1) & (df["date"].dt.date <= d2)]
    if channels:
        df = df[df["channel"].isin(channels)]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Выручка", f"{df['revenue'].sum():,.0f} ₽")
    k2.metric("Расход", f"{df['cost'].sum():,.0f} ₽")
    k3.metric("Заказы", f"{df['orders'].sum():,.0f}")
    k4.metric("ROMI", f"{df['romi'].mean() * 100:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        trend = df.groupby("date", as_index=False)["revenue"].sum()
        st.plotly_chart(px.line(trend, x="date", y="revenue", title="Динамика выручки"), use_container_width=True)
    with col2:
        by_ch = df.groupby("channel", as_index=False)["cost"].sum()
        st.plotly_chart(px.pie(by_ch, names="channel", values="cost", title="Распределение затрат"), use_container_width=True)

    st.subheader("Таблица данных")
    page_size = st.selectbox("Размер страницы", [20, 50, 100], index=1)
    page = st.number_input("Страница", min_value=1, value=1)
    start = (page - 1) * page_size
    st.dataframe(df.iloc[start : start + page_size], use_container_width=True)
    st.download_button("Экспорт CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="dashboard_export.csv")
