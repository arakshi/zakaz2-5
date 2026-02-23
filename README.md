# ВКР-приложение: маркетинговая аналитика e-commerce

Готовое Streamlit-приложение для аналитической обработки маркетинговых данных ООО «Фабрика универсальных покрытий».

## Быстрый старт
```bash
pip install -r requirements.txt
streamlit run app.py
```

По умолчанию используется SQLite (`data/app.db`).

## Опционально PostgreSQL
Установите переменную среды:
```bash
APP_DB_URL=postgresql+psycopg2://user:password@localhost:5432/marketing
```

## Структура
- `core/` — метрики, прогноз, инсайты, демо-данные, конфиг.
- `ui/` — страницы и компоненты интерфейса.
- `connectors/` — коннекторы (demo mock).
- `storage/` — SQLAlchemy и репозиторий.
- `reports/` — HTML-отчеты.
- `tests/` — unit-тесты.
