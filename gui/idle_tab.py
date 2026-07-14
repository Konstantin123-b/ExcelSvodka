from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class IdleTab(QWidget):
    """
    Вкладка переноса простоев.

    Логики работы с Excel здесь нет.
    Вкладка только собирает данные и отправляет их
    в MainWindow через сигнал.
    """

    transfer_requested = Signal(dict)
    garage_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        group = QGroupBox("Перенос простоя")
        form = QFormLayout(group)

        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate())
        form.addRow("С даты", self.from_date)

        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        form.addRow("На дату", self.to_date)

        self.garage = QLineEdit()
        self.garage.setPlaceholderText("Гаражный номер")
        self.garage.textChanged.connect(
            lambda text: self.garage_changed.emit(text.strip())
        )
        form.addRow("Машина", self.garage)

        self.model = QComboBox()
        self.model.setMinimumWidth(260)
        form.addRow("Модель", self.model)

        self.reason = QTextEdit()
        self.reason.setMinimumHeight(120)
        self.reason.setPlaceholderText(
            "При необходимости можно изменить текст простоя..."
        )
        form.addRow("Простой", self.reason)

        buttons = QHBoxLayout()

        self.clear_button = QPushButton("Очистить")
        self.transfer_button = QPushButton("Перенести простой")

        buttons.addStretch()
        buttons.addWidget(self.clear_button)
        buttons.addWidget(self.transfer_button)

        form.addRow(buttons)

        layout.addWidget(group)

        self.info = QLabel(
            "Будут перенесены все простои выбранной машины "
            "с указанной даты на новую."
        )
        self.info.setWordWrap(True)

        layout.addWidget(self.info)
        layout.addStretch()

        self.clear_button.clicked.connect(self.clear_form)
        self.transfer_button.clicked.connect(
            self._emit_transfer
        )

    def clear_form(self):
        self.from_date.setDate(QDate.currentDate())
        self.to_date.setDate(QDate.currentDate())
        self.garage.clear()
        self.model.clear()
        self.reason.clear()

    def set_models(self, models):
        current = self.model.currentText()

        self.model.blockSignals(True)
        self.model.clear()

        added = set()

        for model in models:
            if not model:
                continue

            if model in added:
                continue

            self.model.addItem(model)
            added.add(model)

        index = self.model.findText(current)

        if index >= 0:
            self.model.setCurrentIndex(index)

        self.model.blockSignals(False)

    def _emit_transfer(self):
        self.transfer_requested.emit(
            {
                "from_date": self.from_date.date().toPython(),
                "to_date": self.to_date.date().toPython(),
                "garage": self.garage.text().strip(),
                "model": self.model.currentText().strip(),
                "reason": self.reason.toPlainText().strip(),
            }
        )