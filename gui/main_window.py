from pathlib import Path
from core.equipment_manager import EquipmentManager

from PySide6.QtWidgets import (
    QFileDialog,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import QDate

from core.excel_manager import ExcelManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.excel = ExcelManager()
        self.equipment = None

        self.setWindowTitle("ExcelSvodka")
        self.resize(900, 750)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        title = QLabel("ExcelSvodka")
        title.setStyleSheet(
            "font-size:26px;font-weight:bold;"
        )

        main_layout.addWidget(title)

        self.open_button = QPushButton(
            "Открыть Excel"
        )

        self.open_button.clicked.connect(
            self.open_excel
        )

        main_layout.addWidget(self.open_button)

        self.file_label = QLabel(
            "Файл не открыт"
        )

        main_layout.addWidget(self.file_label)

        group = QGroupBox("Новая работа")

        form = QFormLayout(group)

        self.date = QDateEdit()

        self.date.setCalendarPopup(True)

        self.date.setDate(QDate.currentDate())

        form.addRow("Дата", self.date)

        self.garage = QLineEdit()

        self.garage.textChanged.connect(
        self.on_garage_changed
        )

        form.addRow("Гаражный номер", self.garage)

        self.model = QComboBox()

        form.addRow("Модель", self.model)

        self.code = QComboBox()

        self.code.addItems(
            [
                "",
                "ав",
                "пл",
                "з",
                ">",
            ]
        )

        form.addRow("Код", self.code)

        self.work = QTextEdit()

        self.work.setFixedHeight(120)

        form.addRow("Работа", self.work)

        self.employees = QLineEdit()

        self.employees.setPlaceholderText(
            "Иванов, Петров..."
        )

        form.addRow(
            "Исполнители",
            self.employees,
        )

        self.add_button = QPushButton(
            "Добавить работу"
        )

        form.addRow(self.add_button)

        main_layout.addWidget(group)

        self.status = QLabel("Готов")

        main_layout.addWidget(self.status)

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

            self.equipment = EquipmentManager(self.excel)

            self.file_label.setText(
            Path(filename).name
            )

            self.status.setText(
                "Файл открыт"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e),
            )
    def on_garage_changed(self):

        if self.equipment is None:
            return

        garage = self.garage.text().strip()

        self.model.clear()

        if not garage:
            return

        try:

            machines = self.equipment.find(
                garage_number=garage,
                model=None,
            )

            added = set()

            for machine in machines:

                if machine.model not in added:

                    self.model.addItem(machine.model)

                    added.add(machine.model)

        except Exception:
            pass