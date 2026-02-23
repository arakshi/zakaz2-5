from __future__ import annotations

import pandas as pd


def build_html_report(title: str, kpis: dict[str, float], top_channels: pd.DataFrame, recommendations: pd.DataFrame) -> str:
    kpi_html = "".join([f"<li><b>{k}</b>: {v:,.2f}</li>" for k, v in kpis.items()])
    channels_html = top_channels.to_html(index=False)
    rec_html = recommendations[["channel", "romi", "recommendation"]].to_html(index=False)
    return f"""
    <html lang='ru'>
    <head><meta charset='utf-8'><title>{title}</title></head>
    <body style='font-family:Arial;padding:24px;'>
        <h1>{title}</h1>
        <h2>Ключевые показатели</h2>
        <ul>{kpi_html}</ul>
        <h2>Топ-каналы</h2>
        {channels_html}
        <h2>Рекомендации</h2>
        {rec_html}
    </body>
    </html>
    """
