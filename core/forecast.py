from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


FORECAST_METHODS = {
    "Линейный тренд": "linear",
    "Полиномиальный тренд": "poly",
    "Скользящее среднее": "moving_avg",
}


def _prepare_daily(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    daily = df.groupby("date", as_index=False)[value_col].sum().sort_values("date")
    daily = daily.dropna(subset=[value_col]).copy()
    daily["date"] = pd.to_datetime(daily["date"])
    daily["t"] = np.arange(len(daily))
    return daily


def _forecast_linear(daily: pd.DataFrame, horizon: int) -> pd.DataFrame:
    model = LinearRegression()
    model.fit(daily[["t"]], daily["value"])
    future = pd.DataFrame({"t": np.arange(len(daily), len(daily) + horizon)})
    future["prediction"] = model.predict(future[["t"]]).clip(min=0)
    return future


def _forecast_poly(daily: pd.DataFrame, horizon: int, degree: int) -> pd.DataFrame:
    model = make_pipeline(PolynomialFeatures(degree=degree, include_bias=False), LinearRegression())
    model.fit(daily[["t"]], daily["value"])
    future = pd.DataFrame({"t": np.arange(len(daily), len(daily) + horizon)})
    future["prediction"] = model.predict(future[["t"]]).clip(min=0)
    return future


def _forecast_moving_average(daily: pd.DataFrame, horizon: int, ma_window: int) -> pd.DataFrame:
    vals = daily["value"].tolist()
    preds = []
    for _ in range(horizon):
        start = max(0, len(vals) - ma_window)
        pred = float(np.mean(vals[start:])) if vals else 0.0
        preds.append(max(0.0, pred))
        vals.append(pred)
    return pd.DataFrame({"t": np.arange(len(daily), len(daily) + horizon), "prediction": preds})


def forecast_series(
    df: pd.DataFrame,
    value_col: str,
    horizon: int,
    method: str = "linear",
    poly_degree: int = 2,
    ma_window: int = 7,
) -> pd.DataFrame:
    daily = _prepare_daily(df, value_col).rename(columns={value_col: "value"})
    if daily.empty:
        return pd.DataFrame(columns=["date", "value", "prediction", "lower", "upper", "part"])

    if method == "poly":
        future = _forecast_poly(daily, horizon, poly_degree)
    elif method == "moving_avg":
        future = _forecast_moving_average(daily, horizon, ma_window)
    else:
        future = _forecast_linear(daily, horizon)

    future["date"] = pd.date_range(daily["date"].max() + pd.Timedelta(days=1), periods=horizon)

    residual_std = float((daily["value"] - daily["value"].rolling(7, min_periods=2).mean()).std(skipna=True) or 0)
    future["lower"] = (future["prediction"] - 1.96 * residual_std).clip(lower=0)
    future["upper"] = future["prediction"] + 1.96 * residual_std

    history = daily[["date", "value"]].copy()
    history["prediction"] = np.nan
    history["lower"] = np.nan
    history["upper"] = np.nan
    history["part"] = "history"

    forecast = future[["date", "prediction", "lower", "upper"]].copy()
    forecast["value"] = np.nan
    forecast["part"] = "forecast"

    return pd.concat([history, forecast], ignore_index=True)
