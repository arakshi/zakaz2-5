from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.config import AppConfig
from core.insights import budget_recommendations
from core.metrics import add_marketing_metrics
from storage.repository import fetch_data


def render(config: AppConfig) -> None:
    st.header("Каналы")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return
    df = add_marketing_metrics(df)
    ch = df.groupby("channel", as_index=False).agg(revenue=("revenue", "sum"), cost=("cost", "sum"), orders=("orders", "sum"), conversion=("conversion", "mean"))
    st.plotly_chart(px.bar(ch, x="channel", y=["revenue", "cost"], barmode="group", title="Доход и расход по каналам"), use_container_width=True)
    rec = budget_recommendations(df)
    st.subheader("Рекомендации по бюджету")
    st.dataframe(rec, use_container_width=True)
