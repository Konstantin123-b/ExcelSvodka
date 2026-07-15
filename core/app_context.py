from __future__ import annotations

from core.excel_manager import ExcelManager
from core.settings_manager import SettingsManager
from core.svodka_manager import SvodkaManager


class AppContext:
    """
    Центральный контейнер приложения.

    Создается один раз
    при запуске программы.
    """

    def __init__(self):

        self.settings = SettingsManager()

        self.excel = ExcelManager()

        self.svodka = SvodkaManager(
            self.excel
        )