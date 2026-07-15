from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class InfoPanel(QFrame):
    """
    Верхняя информационная панель вкладки "Сводка".
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()

    # ---------------------------------------------------------

    def _build_ui(self):

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        self.file_label = QLabel("Файл: -")
        self.date_label = QLabel("Дата: -")
        self.total_label = QLabel("Общее кол-во техники: 0")
        self.idle_label = QLabel("Общее кол-во техники в простое: 0")

        for label in (
            self.file_label,
            self.date_label,
            self.total_label,
            self.idle_label,
        ):
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            layout.addWidget(label)

        layout.addStretch()

    # ---------------------------------------------------------

    def set_file(self, filename: str):

        self.file_label.setText(
            f"Файл: {filename}"
        )

    # ---------------------------------------------------------

    def set_date(self, date: str):

        self.date_label.setText(
            f"Дата: {date}"
        )

    # ---------------------------------------------------------

    def set_total(self, count: int):

        self.total_label.setText(
            f"Общее кол-во техники: {count}"
        )

    # ---------------------------------------------------------

    def set_idle(self, count: int):

        self.idle_label.setText(
            f"Общее кол-во техники в простое: {count}"
        )

    # ---------------------------------------------------------

    def update_info(
        self,
        filename: str,
        date: str,
        total: int,
        idle: int,
    ):

        self.set_file(filename)
        self.set_date(date)
        self.set_total(total)
        self.set_idle(idle)