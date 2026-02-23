from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression


def forecast_series(df: pd.DataFrame, value_col: str, horizon: int) -> pd.DataFrame:
    daily = df.groupby("date", as_index=False)[value_col].sum().sort_values("date")
    daily = daily.dropna()
    if daily.empty:
        return pd.DataFrame(columns=["date", "value", "prediction"])

    daily["t"] = range(len(daily))
    model = LinearRegression()
    model.fit(daily[["t"]], daily[value_col])

    future = pd.DataFrame({"t": range(len(daily), len(daily) + horizon)})
    future["date"] = pd.date_range(daily["date"].max() + pd.Timedelta(days=1), periods=horizon)
    future["prediction"] = model.predict(future[["t"]]).clip(min=0)

    history = daily[["date", value_col]].rename(columns={value_col: "value"})
    history["prediction"] = None
    forecast = future[["date"]].copy()
    forecast["value"] = None
    forecast["prediction"] = future["prediction"]
    return pd.concat([history, forecast], ignore_index=True)
