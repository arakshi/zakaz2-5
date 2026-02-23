from __future__ import annotations

import streamlit as st

from core.config import AppConfig


def render_topbar(config: AppConfig) -> None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Аналитическая платформа e-commerce")
        st.caption("ООО «Фабрика универсальных покрытий»")
    with col2:
        st.selectbox("Роль", ["администратор", "маркетолог", "аналитик"], key="role")


def date_filters(df):
    st.sidebar.subheader("Фильтры")
    if df.empty:
        return None, None, []
    min_d = df["date"].min().date()
    max_d = df["date"].max().date()
    period = st.sidebar.date_input("Период", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    ch = st.sidebar.multiselect("Каналы", sorted(df["channel"].dropna().unique().tolist()))
    return period[0], period[1], ch
