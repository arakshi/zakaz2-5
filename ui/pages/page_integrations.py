from __future__ import annotations

import pandas as pd
import streamlit as st

from connectors.mock_sources import VKAdsConnector, YandexDirectConnector, YandexMetrikaConnector
from core.config import AppConfig
from core.metrics import ensure_schema
from storage.repository import append_manual_row, import_sqlite_database, upsert_dataframe


MANUAL_FIELDS = [
    "date",
    "channel",
    "campaign",
    "region",
    "device",
    "sessions",
    "orders",
    "revenue",
    "cost",
    "users",
    "new_users",
]


def render(config: AppConfig) -> None:
    st.header("Интеграции")
    st.info("Коннекторы работают в demo-режиме. Для боевого режима используйте токены в переменных окружения.")

    connectors = [YandexMetrikaConnector(), YandexDirectConnector(), VKAdsConnector()]
    for connector in connectors:
        if st.button(f"Загрузить данные: {connector.name}"):
            data = connector.fetch("2024-01-01", "2025-12-31")
            upsert_dataframe(config, ensure_schema(data), connector.name)
            st.success(f"Импортировано из {connector.name}: {len(data)} строк")

    st.subheader("Ручной ввод продаж/трафика")
    with st.form("manual_add_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            date = st.date_input("Дата")
            channel = st.text_input("Канал", value="manual")
            campaign = st.text_input("Кампания", value="Ручной ввод")
            region = st.text_input("Регион", value="Москва")
        with c2:
            device = st.selectbox("Устройство", ["desktop", "mobile", "tablet"])
            sessions = st.number_input("Сессии (трафик)", min_value=0, value=100)
            users = st.number_input("Пользователи", min_value=0, value=80)
            new_users = st.number_input("Новые пользователи", min_value=0, value=20)
        with c3:
            orders = st.number_input("Заказы", min_value=0, value=10)
            revenue = st.number_input("Выручка", min_value=0.0, value=50000.0, step=1000.0)
            cost = st.number_input("Расход", min_value=0.0, value=12000.0, step=500.0)
        submitted = st.form_submit_button("Добавить запись")

    if submitted:
        row = {
            "date": pd.to_datetime(date),
            "channel": channel,
            "campaign": campaign,
            "region": region,
            "device": device,
            "sessions": sessions,
            "orders": orders,
            "revenue": revenue,
            "cost": cost,
            "users": users,
            "new_users": new_users,
        }
        append_manual_row(config, row)
        st.success("Ручная запись добавлена в базу.")

    st.subheader("Загрузка существующей SQLite базы")
    uploaded_db = st.file_uploader("Загрузить .db / .sqlite", type=["db", "sqlite", "sqlite3"], key="upload_sqlite")
    table_name = st.text_input("Имя таблицы в загружаемой БД", value="marketing_raw")
    if uploaded_db is not None and st.button("Импортировать базу"):
        try:
            rows = import_sqlite_database(config, uploaded_db.getvalue(), table_name=table_name)
            st.success(f"База импортирована: {rows} строк")
        except Exception as exc:
            st.error(f"Ошибка импорта базы: {exc}")

    st.subheader("Универсальный импорт файлов")
    uploaded = st.file_uploader("Загрузить CSV/XLSX/JSON", type=["csv", "xlsx", "json"], key="upload_files")
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        elif uploaded.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_json(uploaded)

        st.write("Сопоставление колонок")
        mapped = {}
        for col in MANUAL_FIELDS:
            mapped[col] = st.selectbox(f"{col}", options=["<пусто>"] + df.columns.tolist(), key=f"map_{col}")
        if st.button("Сохранить импорт"):
            out = pd.DataFrame()
            for target, source in mapped.items():
                out[target] = df[source] if source != "<пусто>" else None
            clean = ensure_schema(out)
            upsert_dataframe(config, clean, uploaded.name, uploaded.getvalue())
            st.success(f"Сохранено: {len(clean)} строк")
