from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class SvodkaToolbar(QWidget):

    add_clicked = Signal()
    remove_clicked = Signal()
    build_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.add_button = QPushButton("➕ Новая запись")
        self.remove_button = QPushButton("🗑 Удалить")
        self.build_button = QPushButton("📄 Сформировать сводку")

        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)

        layout.addStretch()

        layout.addWidget(self.build_button)

        self.add_button.clicked.connect(
            self.add_clicked
        )

        self.remove_button.clicked.connect(
            self.remove_clicked
        )

        self.build_button.clicked.connect(
            self.build_clicked
        )