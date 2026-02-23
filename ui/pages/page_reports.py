from __future__ import annotations

import streamlit as st

from core.config import AppConfig
from core.insights import budget_recommendations
from reports.html_report import build_html_report
from storage.repository import fetch_data, load_reports, save_report


def render(config: AppConfig) -> None:
    st.header("Отчеты")
    df = fetch_data(config)
    if df.empty:
        st.info("Нет данных")
        return

    c1, c2 = st.columns(2)
    with c1:
        start = st.date_input("Дата начала")
    with c2:
        end = st.date_input("Дата окончания")

    if st.button("Сгенерировать HTML-отчет"):
        kpis = {
            "Выручка": float(df["revenue"].sum()),
            "Расход": float(df["cost"].sum()),
            "Заказы": float(df["orders"].sum()),
        }
        top = df.groupby("channel", as_index=False).agg(revenue=("revenue", "sum")).sort_values("revenue", ascending=False)
        rec = budget_recommendations(df)
        html = build_html_report("Отчет по маркетингу", kpis, top, rec)
        save_report(config, str(start), str(end), html)
        st.download_button("Скачать HTML", data=html.encode("utf-8"), file_name="report.html", mime="text/html")

    st.subheader("История отчетов")
    st.dataframe(load_reports(config), use_container_width=True)
