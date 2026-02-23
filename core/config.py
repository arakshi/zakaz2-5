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


def apply_theme() -> None:
    """Фиксированная современная светлая тема без переключателя в UI."""
    st.markdown(
        """
        <style>
            .stApp {background-color: #f7fafc; color: #0f172a;}
            [data-testid="stMetric"] {
                background: #ffffff;
                border-radius: 14px;
                padding: 10px;
                border: 1px solid #e2e8f0;
            }
            .main .block-container {padding-top: 1rem;}
            .stButton>button {
                border-radius: 10px;
                border: 1px solid #2563eb;
            }
            [data-testid="stSidebar"] {border-right: 1px solid #cbd5e1;}
        </style>
        """,
        unsafe_allow_html=True,
    )
