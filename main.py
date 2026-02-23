from __future__ import annotations

import os
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def run() -> None:
    """Запуск приложения одной кнопкой Run в PyCharm.

    Достаточно запустить этот файл как обычный Python-скрипт.
    """
    root = Path(__file__).resolve().parent
    app_path = root / "app.py"

    os.chdir(root)
    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    raise SystemExit(stcli.main())


if __name__ == "__main__":
    run()
