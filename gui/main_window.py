from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from core.excel_manager import ExcelManager
from core.settings_manager import SettingsManager
from core.svodka_manager import SvodkaManager

from gui.settings_tab import SettingsTab
from gui.svodka_tab import SvodkaTab

from PySide6.QtWidgets import QMessageBox


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.settings = SettingsManager()

        self.excel = ExcelManager()

        self.manager = None

        self.setWindowTitle(
            "ExcelSvodka 2.0"
        )

        width, height = self.settings.window_size

        self.resize(
            width,
            height,
        )

        self.tabs = QTabWidget()

        self.setCentralWidget(
            self.tabs
        )

        self.svodka_tab = SvodkaTab()

        self.settings_tab = SettingsTab()

        self.tabs.addTab(
            self.svodka_tab,
            "Ежедневная сводка",
        )

        self.tabs.addTab(
            self.settings_tab,
            "Настройки",
        )

        self.file_label = QLabel(
            "Файл не открыт"
        )

        self.status = QStatusBar()

        self.setStatusBar(
            self.status
        )

        self.status.addPermanentWidget(
            self.file_label
        )

        self.open_excel()
            
    # ---------------------------------------------------------

    def open_excel(self):

        filename = self.settings.last_file

        if filename and Path(filename).exists():

            self.load_excel(
                filename
            )

            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть Excel",
            "",
            "Excel (*.xlsx *.xlsm)",
        )

        if not filename:
            return

        self.load_excel(
            filename
        )

    # ---------------------------------------------------------

    def load_excel(
        self,
        filename: str,
    ):

        try:

            self.excel.open(
                filename
            )

            self.manager = SvodkaManager(
                self.excel
            )

            self.svodka_tab.set_manager(
                self.manager
            )

            self.settings.last_file = filename

            self.file_label.setText(
                Path(filename).name
            )

            self.status.showMessage(
                "Файл открыт",
                3000,
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )

    # ---------------------------------------------------------

    def closeEvent(self, event):

        if (
            self.manager is not None
            and self.manager.is_modified()
        ):

            result = QMessageBox.question(
                self,
                "Несохраненные изменения",
                "Есть несохраненные изменения.\n\n"
                "Сохранить их перед выходом?",
                QMessageBox.Yes
                | QMessageBox.No
                | QMessageBox.Cancel,
                QMessageBox.Yes,
            )

            if result == QMessageBox.Cancel:
                event.ignore()
                return

            if result == QMessageBox.Yes:

                try:
                    self.manager.build(
                        self.svodka_tab.current_date()
                    )

                except Exception as e:

                    QMessageBox.critical(
                        self,
                        "Ошибка",
                        str(e),
                    )

                    event.ignore()
                    return

        self.settings.window_size = (
            self.width(),
            self.height(),
        )

        super().closeEvent(event)

    def show_error(
        self,
        text: str,
    ):

        QMessageBox.critical(
            self,
            "ExcelSvodka",
            text,
        )

    # ---------------------------------------------------------

    def show_info(
        self,
        text: str,
    ):

        QMessageBox.information(
            self,
            "ExcelSvodka",
            text,
        )