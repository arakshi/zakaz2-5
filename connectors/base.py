from __future__ import annotations

from abc import ABC, abstractmethod
import pandas as pd


class BaseConnector(ABC):
    name: str

    @abstractmethod
    def fetch(self, start_date: str, end_date: str) -> pd.DataFrame:
        raise NotImplementedError
