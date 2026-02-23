from __future__ import annotations

import pandas as pd
import streamlit as st

from connectors.mock_sources import VKAdsConnector, YandexDirectConnector, YandexMetrikaConnector
from core.config import AppConfig
from core.metrics import ensure_schema
from storage.repository import upsert_dataframe


def render(config: AppConfig) -> None:
    st.header("Интеграции")
    st.info("Коннекторы работают в demo-режиме. Для боевого режима используйте токены в переменных окружения.")

    connectors = [YandexMetrikaConnector(), YandexDirectConnector(), VKAdsConnector()]
    for connector in connectors:
        if st.button(f"Загрузить данные: {connector.name}"):
            data = connector.fetch("2024-01-01", "2025-12-31")
            upsert_dataframe(config, ensure_schema(data), connector.name)
            st.success(f"Импортировано из {connector.name}: {len(data)} строк")

    st.subheader("Универсальный импорт файлов")
    uploaded = st.file_uploader("Загрузить CSV/XLSX/JSON", type=["csv", "xlsx", "json"])
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        elif uploaded.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_json(uploaded)

        st.write("Сопоставление колонок")
        mapped = {}
        for col in ["date", "channel", "campaign", "region", "device", "sessions", "orders", "revenue", "cost", "users", "new_users"]:
            mapped[col] = st.selectbox(f"{col}", options=["<пусто>"] + df.columns.tolist(), key=f"map_{col}")
        if st.button("Сохранить импорт"):
            out = pd.DataFrame()
            for target, source in mapped.items():
                out[target] = df[source] if source != "<пусто>" else None
            clean = ensure_schema(out)
            upsert_dataframe(config, clean, uploaded.name, uploaded.getvalue())
            st.success(f"Сохранено: {len(clean)} строк")
