from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st


@dataclass
class AppConfig:
    db_url: str
    yandex_metrika_token: str = ""
    yandex_direct_token: str = ""
    vk_ads_token: str = ""


def load_runtime_config() -> AppConfig:
    db_url = os.getenv("APP_DB_URL", "sqlite:///data/app.db")
    return AppConfig(
        db_url=db_url,
        yandex_metrika_token=os.getenv("YANDEX_METRIKA_TOKEN", ""),
        yandex_direct_token=os.getenv("YANDEX_DIRECT_TOKEN", ""),
        vk_ads_token=os.getenv("VK_ADS_TOKEN", ""),
    )


def apply_theme(theme_name: str) -> None:
    dark = theme_name == "Тёмная"
    bg = "#0f172a" if dark else "#f7fafc"
    fg = "#f8fafc" if dark else "#0f172a"
    card = "#1e293b" if dark else "#ffffff"
    accent = "#2563eb"

    st.markdown(
        f"""
        <style>
            .stApp {{background-color: {bg}; color: {fg};}}
            [data-testid="stMetric"] {{background: {card}; border-radius: 14px; padding: 10px;}}
            .main .block-container {{padding-top: 1rem;}}
            .stButton>button {{border-radius: 10px; border: 1px solid {accent};}}
            [data-testid="stSidebar"] {{border-right: 1px solid #334155;}}
        </style>
        """,
        unsafe_allow_html=True,
    )
