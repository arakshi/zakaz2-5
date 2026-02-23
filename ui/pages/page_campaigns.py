from __future__ import annotations

import plotly.express as px
import streamlit as st

from core.config import AppConfig
from core.metrics import add_marketing_metrics
from storage.repository import fetch_data


def render(config: AppConfig) -> None:
    st.header("Кампании")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return
    df = add_marketing_metrics(df)
    camp = df.groupby("campaign", as_index=False).agg(revenue=("revenue", "sum"), cost=("cost", "sum"), orders=("orders", "sum"), romi=("romi", "mean"))
    st.plotly_chart(px.scatter(camp, x="cost", y="revenue", size="orders", color="romi", hover_name="campaign", title="Эффективность кампаний"), use_container_width=True)
    st.dataframe(camp.sort_values("romi", ascending=False), use_container_width=True)
