from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class WorkTab(QWidget):
    """
    Вкладка добавления выполненных работ.
    """

    add_requested = Signal(dict)
    garage_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        group = QGroupBox("Новая работа")
        form = QFormLayout(group)

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())
        form.addRow("Дата", self.date)

        self.garage = QLineEdit()
        self.garage.setPlaceholderText("Например: D475 №3216")
        self.garage.textChanged.connect(
            lambda text: self.garage_changed.emit(text.strip())
        )
        form.addRow("Гаражный номер", self.garage)

        self.model = QComboBox()
        self.model.setMinimumWidth(260)
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
        self.work.setMinimumHeight(140)
        form.addRow("Работа", self.work)

        self.employees = QLineEdit()
        self.employees.setPlaceholderText("Кузнецов, Иванов...")
        form.addRow("Исполнители", self.employees)

        buttons = QHBoxLayout()

        self.clear_button = QPushButton("Очистить")
        self.add_button = QPushButton("Добавить работу")

        buttons.addStretch()
        buttons.addWidget(self.clear_button)
        buttons.addWidget(self.add_button)

        form.addRow(buttons)

        layout.addWidget(group)
        layout.addStretch()

        self.clear_button.clicked.connect(self.clear_form)
        self.add_button.clicked.connect(self._emit_add)

    def set_models(self, models):

        current = self.model.currentText()

        self.model.blockSignals(True)
        self.model.clear()

        added = set()

        for item in models:
            if not item:
                continue

            if item in added:
                continue

            self.model.addItem(item)
            added.add(item)

        index = self.model.findText(current)

        if index >= 0:
            self.model.setCurrentIndex(index)

        self.model.blockSignals(False)

    def clear_form(self):
        self.garage.clear()
        self.model.clear()
        self.code.setCurrentIndex(0)
        self.work.clear()
        self.employees.clear()
        self.date.setDate(QDate.currentDate())

    def _emit_add(self):

        self.add_requested.emit(
            {
                "date": self.date.date().toString("dd.MM.yyyy"),
                "garage": self.garage.text().strip(),
                "model": self.model.currentText().strip(),
                "code": self.code.currentText().strip(),
                "work": self.work.toPlainText().strip(),
                "employees": self.employees.text().strip(),
            }
        )
