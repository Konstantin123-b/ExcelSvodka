from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class DateSelector(QWidget):

    date_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        layout.addWidget(QLabel("Дата:"))

        self.date_edit = QDateEdit()

        self.date_edit.setCalendarPopup(True)

        self.date_edit.setDisplayFormat(
            "dd.MM.yyyy"
        )

        self.date_edit.setDate(
            QDate.currentDate()
        )

        layout.addWidget(self.date_edit)

        layout.addStretch()

        self.date_edit.dateChanged.connect(
            self._on_date_changed
        )

    # ---------------------------------------------------------

    def date_string(self) -> str:

        return self.date_edit.date().toString(
            "dd.MM.yyyy"
        )

    # ---------------------------------------------------------

    def set_date(
        self,
        date: QDate,
    ):

        self.date_edit.setDate(date)

    # ---------------------------------------------------------

    def _on_date_changed(
        self,
        _,
    ):

        self.date_changed.emit(
            self.date_string()
        )