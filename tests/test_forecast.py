import pandas as pd

from core.forecast import forecast_series


def test_forecast_horizon():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=20),
            "revenue": list(range(100, 120)),
        }
    )
    out = forecast_series(df, "revenue", 7)
    assert len(out[out["prediction"].notna()]) == 7
