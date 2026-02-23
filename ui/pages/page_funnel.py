from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.config import AppConfig
from storage.repository import fetch_data


def render(config: AppConfig) -> None:
    st.header("Воронка")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return
    sessions = df["sessions"].sum()
    users = df["users"].sum()
    orders = df["orders"].sum()
    fig = go.Figure(go.Funnel(y=["Трафик", "Пользователи", "Заказы"], x=[sessions, users, orders]))
    fig.update_layout(title="Воронка от трафика к заказу")
    st.plotly_chart(fig, use_container_width=True)
