from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from core.config import AppConfig
from core.metrics import build_cohort
from storage.repository import fetch_data


def render(config: AppConfig) -> None:
    st.header("Когортный анализ")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return
    df["date"] = pd.to_datetime(df["date"])
    cohort = build_cohort(df)
    fig = px.imshow(cohort.values, x=cohort.columns, y=cohort.index, color_continuous_scale="Blues", title="Retention Heatmap")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(cohort, use_container_width=True)
