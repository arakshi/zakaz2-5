from __future__ import annotations

import streamlit as st

from core.config import AppConfig, apply_theme, load_runtime_config
from storage.db import init_db
from ui.layout import render_topbar
from ui.pages import (
    page_campaigns,
    page_channels,
    page_cohorts,
    page_dashboard,
    page_demo,
    page_forecast,
    page_funnel,
    page_integrations,
    page_reports,
    page_settings,
)

PAGES = {
    "Дашборд": page_dashboard.render,
    "Каналы": page_channels.render,
    "Кампании": page_campaigns.render,
    "Воронка": page_funnel.render,
    "Когорты": page_cohorts.render,
    "Прогноз": page_forecast.render,
    "Отчеты": page_reports.render,
    "Интеграции": page_integrations.render,
    "Настройки": page_settings.render,
    "Демо": page_demo.render,
}

ROLE_ACCESS = {
    "администратор": set(PAGES.keys()),
    "маркетолог": {"Дашборд", "Каналы", "Кампании", "Воронка", "Прогноз", "Отчеты", "Демо", "Интеграции"},
    "аналитик": {"Дашборд", "Каналы", "Кампании", "Воронка", "Когорты", "Прогноз", "Отчеты", "Демо"},
}


def bootstrap() -> AppConfig:
    st.set_page_config(
        page_title="Маркетинг-Аналитика ФУП",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    if "role" not in st.session_state:
        st.session_state.role = "администратор"
    if "theme" not in st.session_state:
        st.session_state.theme = "Светлая"
    runtime = load_runtime_config()
    init_db(runtime)
    apply_theme(st.session_state.theme)
    return runtime


def main() -> None:
    runtime = bootstrap()
    render_topbar(runtime)

    role = st.session_state.role
    available_pages = [name for name in PAGES if name in ROLE_ACCESS.get(role, set())]

    with st.sidebar:
        st.title("Меню")
        selected = st.radio("Раздел", options=available_pages)

    PAGES[selected](runtime)


if __name__ == "__main__":
    main()
