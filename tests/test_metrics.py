import pandas as pd

from core.metrics import add_marketing_metrics


def test_metrics_calculation():
    df = pd.DataFrame(
        [
            {
                "date": "2024-01-01",
                "channel": "A",
                "campaign": "C1",
                "region": "Москва",
                "device": "mobile",
                "sessions": 100,
                "orders": 10,
                "revenue": 50000,
                "cost": 10000,
                "users": 80,
                "new_users": 20,
            }
        ]
    )
    out = add_marketing_metrics(df)
    assert out.loc[0, "conversion"] == 0.1
    assert out.loc[0, "cac"] == 1000
    assert out.loc[0, "aov"] == 5000
