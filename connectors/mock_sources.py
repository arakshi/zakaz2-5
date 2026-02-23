from __future__ import annotations

import pandas as pd

from core.demo_data import generate_demo_data
from connectors.base import BaseConnector


class YandexMetrikaConnector(BaseConnector):
    name = "Яндекс Метрика"

    def fetch(self, start_date: str, end_date: str) -> pd.DataFrame:
        df = generate_demo_data(days=120, seed=1)
        return df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()


class YandexDirectConnector(BaseConnector):
    name = "Яндекс Директ"

    def fetch(self, start_date: str, end_date: str) -> pd.DataFrame:
        df = generate_demo_data(days=120, seed=2)
        return df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()


class VKAdsConnector(BaseConnector):
    name = "VK Реклама"

    def fetch(self, start_date: str, end_date: str) -> pd.DataFrame:
        df = generate_demo_data(days=120, seed=3)
        return df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()
