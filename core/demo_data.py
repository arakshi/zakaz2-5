from __future__ import annotations

import numpy as np
import pandas as pd


CHANNELS = ["Яндекс Директ", "VK Реклама", "SEO", "Email", "Маркетплейс"]
REGIONS = ["Москва", "Санкт-Петербург", "Казань", "Екатеринбург", "Новосибирск"]
DEVICES = ["desktop", "mobile", "tablet"]


def generate_demo_data(days: int = 365, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    rows = []
    for date in dates:
        for ch in CHANNELS:
            sessions = int(rng.integers(300, 3000))
            conversion_rate = rng.uniform(0.01, 0.08)
            orders = int(sessions * conversion_rate)
            aov = rng.uniform(2500, 12000)
            revenue = orders * aov
            cost = sessions * rng.uniform(8, 90)
            users = int(sessions * rng.uniform(0.6, 0.95))
            new_users = int(users * rng.uniform(0.1, 0.4))
            rows.append(
                {
                    "date": date,
                    "channel": ch,
                    "campaign": f"{ch} / Кампания {rng.integers(1, 8)}",
                    "region": rng.choice(REGIONS),
                    "device": rng.choice(DEVICES),
                    "sessions": sessions,
                    "orders": orders,
                    "revenue": round(revenue, 2),
                    "cost": round(cost, 2),
                    "users": users,
                    "new_users": new_users,
                }
            )
    return pd.DataFrame(rows)
