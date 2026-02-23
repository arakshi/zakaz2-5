from __future__ import annotations

import streamlit as st

from core.config import AppConfig


def render(config: AppConfig) -> None:
    st.header("Настройки")
    st.write("### Конфигурация подключений")
    st.code(
        """
APP_DB_URL=sqlite:///data/app.db
YANDEX_METRIKA_TOKEN=...
YANDEX_DIRECT_TOKEN=...
VK_ADS_TOKEN=...
        """
    )
    st.success(f"Текущая БД: {config.db_url}")
