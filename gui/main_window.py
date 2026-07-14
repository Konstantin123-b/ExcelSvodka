from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from core.equipment_manager import EquipmentManager
from core.excel_manager import ExcelManager
from core.svodka_engine import SvodkaEngine

from gui.work_tab import WorkTab
from gui.idle_tab import IdleTab
from gui.settings_tab import SettingsTab


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.excel = ExcelManager()
        self.equipment = None
        self.engine = None

        self.setWindowTitle("ExcelSvodka")
        self.resize(1100, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("ExcelSvodka")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size:26px;font-weight:bold;"
        )

        layout.addWidget(title)

        top = QHBoxLayout()

        self.open_button = QPushButton("Открыть Excel")
        self.open_button.clicked.connect(self.open_excel)

        self.file_label = QLabel("Файл не открыт")

        top.addWidget(self.open_button)
        top.addWidget(self.file_label)

        layout.addLayout(top)

        self.tabs = QTabWidget()

        self.work_tab = WorkTab()
        self.idle_tab = IdleTab()
        self.settings_tab = SettingsTab()

        self.tabs.addTab(self.work_tab, "Работы")
        self.tabs.addTab(self.idle_tab, "Простои")
        self.tabs.addTab(self.settings_tab, "Настройки")

        layout.addWidget(self.tabs)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(170)

        layout.addWidget(self.log)

        self.status = QLabel("Готов")
        layout.addWidget(self.status)

        self.work_tab.garage_changed.connect(
            self.update_models
        )

        self.idle_tab.garage_changed.connect(
            self.update_models
        )

        self.work_tab.add_requested.connect(
            self.on_add_work
        )

        self.idle_tab.transfer_requested.connect(
            self.on_transfer_idle
        )

        self.settings_tab.settings_changed.connect(
            self.on_settings_changed
        )

        self.log_message("Приложение запущено.")

    def log_message(self, text):
        self.log.append(text)

    def open_excel(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите Excel",
            "",
            "Excel (*.xlsx *.xlsm)",
        )

        if not filename:
            return

        try:

            self.excel.open(filename)

            self.equipment = EquipmentManager(
                self.excel
            )

            self.engine = SvodkaEngine(
                self.excel
            )

            self.file_label.setText(
                Path(filename).name
            )

            self.status.setText("Файл открыт")

            self.log_message(
                f"Открыт файл: {filename}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e),
            )

    def update_models(self, garage):

        if self.equipment is None:
            return

        garage = garage.strip()

        if not garage:
            self.work_tab.set_models([])
            self.idle_tab.set_models([])
            return

        try:

            machines = self.equipment.find(
                garage_number=garage,
                model=None,
            )

            models = []
            added = set()

            for machine in machines:

                if machine.model in added:
                    continue

                models.append(machine.model)
                added.add(machine.model)

            self.work_tab.set_models(models)
            self.idle_tab.set_models(models)

        except Exception as e:

            self.log_message(
                f"Ошибка поиска техники: {e}"
            )

    def on_add_work(self, data):

        if self.engine is None:

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                "Сначала откройте файл Excel."
            )

            return

        try:

            self.engine.add_work(
                garage_number=data["garage"],
                model=data["model"],
                date=data["date"],
                code=data["code"],
                work=data["work"],
                employees=data["employees"],
            )

            self.engine.apply_changes()

            self.engine.save()

            self.log_message(
                f"✔ Работа добавлена: {data['garage']}"
            )

            self.status.setText(
                "Работа успешно добавлена"
            )

            QMessageBox.information(
                self,
                "ExcelSvodka",
                "Работа успешно записана."
            )

            self.work_tab.clear_form()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e),
            )

            self.log_message(
                f"Ошибка: {e}"
            )
    def on_transfer_idle(self, data):

        if self.engine is None:

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                "Сначала откройте файл Excel."
            )

            return

        try:

            # Пока только журнал.
            # После подключения IdleTransferManager
            # здесь будет реальный перенос простоев.

            self.log_message(
                f"Перенос простоя: {data}"
            )

            self.status.setText(
                "Перенос простоя выполнен"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e),
            )

            self.log_message(
                f"Ошибка переноса: {e}"
            )

    def on_settings_changed(self, settings):

        self.log_message(
            "Настройки сохранены."
        )

    def closeEvent(self, event):

        try:

            if self.excel is not None:
                self.excel.save()

        except Exception as e:

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                f"Не удалось сохранить файл:\n{e}",
            )

        event.accept()
