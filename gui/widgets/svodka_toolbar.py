from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class SvodkaToolbar(QWidget):

    add_clicked = Signal()
    remove_clicked = Signal()
    reload_clicked = Signal()
    build_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.add_button = QPushButton("Новая запись")
        self.remove_button = QPushButton("Удалить")
        self.reload_button = QPushButton("Обновить из Excel")
        self.build_button = QPushButton("Сформировать сводку")

        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.reload_button)

        layout.addStretch()

        layout.addWidget(self.build_button)

        self.add_button.clicked.connect(
            self.add_clicked.emit
        )

        self.remove_button.clicked.connect(
            self.remove_clicked.emit
        )

        self.reload_button.clicked.connect(
            self.reload_clicked.emit
        )

        self.build_button.clicked.connect(
            self.build_clicked.emit
        )