import pandas as pd

from core.forecast import forecast_series


def _df():
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=30),
            "revenue": list(range(100, 130)),
        }
    )


def test_forecast_horizon_linear():
    out = forecast_series(_df(), "revenue", 7, method="linear")
    assert len(out[out["part"] == "forecast"]) == 7


def test_forecast_horizon_poly():
    out = forecast_series(_df(), "revenue", 10, method="poly", poly_degree=3)
    assert len(out[out["part"] == "forecast"]) == 10


def test_forecast_horizon_moving_average():
    out = forecast_series(_df(), "revenue", 5, method="moving_avg", ma_window=5)
    future = out[out["part"] == "forecast"]
    assert len(future) == 5
    assert (future["prediction"] >= 0).all()
