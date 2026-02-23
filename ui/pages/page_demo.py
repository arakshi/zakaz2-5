from __future__ import annotations

import streamlit as st

from core.config import AppConfig
from core.demo_data import generate_demo_data
from core.metrics import ensure_schema
from storage.repository import upsert_dataframe


SCENARIO = [
    "1) Сгенерируйте демо-данные.",
    "2) Откройте Дашборд и покажите KPI.",
    "3) Перейдите в Каналы и покажите рекомендации.",
    "4) Откройте Воронку и Когорты.",
    "5) В Прогнозе выберите горизонт 90 дней.",
    "6) В Отчетах сформируйте HTML-файл.",
]


def render(config: AppConfig) -> None:
    st.header("Демо")
    st.write("### Сценарий демонстрации для защиты")
    for step in SCENARIO:
        st.write(step)

    days = st.slider("Глубина данных (дней)", 60, 730, 365)
    if st.button("Сгенерировать и загрузить демо-данные"):
        df = generate_demo_data(days=days)
        upsert_dataframe(config, ensure_schema(df), f"demo_{days}")
        st.success(f"Готово: {len(df)} строк загружено в базу")
