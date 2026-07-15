from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.excel_manager import ExcelManager
from core.svodka_manager import SvodkaManager

from gui.settings_tab import SettingsTab
from gui.svodka_tab import SvodkaTab


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.excel = ExcelManager()
        self.manager = None

        self.setWindowTitle("ExcelSvodka 2.0")
        self.resize(1400, 900)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("ExcelSvodka 2.0")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
            """
        )
        layout.addWidget(title)

        top = QHBoxLayout()

        self.open_button = QPushButton("Открыть Excel")
        self.open_button.clicked.connect(self.open_excel)

        self.file_label = QLabel("Файл не открыт")

        top.addWidget(self.open_button)
        top.addWidget(self.file_label, 1)

        layout.addLayout(top)

        self.tabs = QTabWidget()

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

        layout.addWidget(self.tabs)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(180)

        layout.addWidget(self.log)

        self.status = QLabel("Готов")
        layout.addWidget(self.status)

        self.settings_tab.settings_changed.connect(
            self.on_settings_changed
        )

        self.log_message(
            "ExcelSvodka 2.0 запущена."
        )

    # ---------------------------------------------------------

    def log_message(
        self,
        text: str,
    ):
        self.log.append(text)

    # ---------------------------------------------------------

    def open_excel(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл Excel",
            "",
            "Excel (*.xlsx *.xlsm)",
        )

        if not filename:
            return

        try:

            self.excel.open(filename)

            self.manager = SvodkaManager(
                self.excel
            )

            self.svodka_tab.set_manager(
                self.manager
            )

            self.file_label.setText(
                Path(filename).name
            )

            self.status.setText(
                "Excel открыт"
            )

            self.log_message(
                f"Открыт файл:\n{filename}"
            )

        except Exception as e:

            self.show_error(str(e))

    # ---------------------------------------------------------

    def on_settings_changed(
        self,
        settings,
    ):
        self.log_message(
            "Настройки сохранены."
        )

    # ---------------------------------------------------------

    def show_error(
        self,
        text: str,
    ):

        QMessageBox.critical(
            self,
            "ExcelSvodka",
            text,
        )

        self.log_message(text)

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

        self.log_message(text)