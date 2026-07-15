from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SvodkaTab(QWidget):

    HEADERS = (
        "Тип",
        "Модель",
        "Гаражный №",
        "Описание",
        "Наработка",
        "Исполнители",
    )

    def __init__(self, parent=None):

        super().__init__(parent)

        self.manager = None

        root = QVBoxLayout(self)

        group = QGroupBox(
            "Ежедневная сводка"
        )

        layout = QVBoxLayout(group)

        top = QHBoxLayout()

        top.addWidget(
            QLabel("Дата")
        )

        self.date = QDateEdit()

        self.date.setCalendarPopup(True)

        self.date.setDate(
            QDate.currentDate()
        )

        top.addWidget(
            self.date
        )

        top.addStretch()

        layout.addLayout(top)

        self.info = QLabel(
            ""
        )

        layout.addWidget(
            self.info
        )

        self.table = QTableWidget()

        self.table.setColumnCount(
            len(self.HEADERS)
        )

        self.table.setHorizontalHeaderLabels(
            self.HEADERS
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
        )

        self.table.verticalHeader().setVisible(
            False
        )

        layout.addWidget(
            self.table
        )
                buttons = QHBoxLayout()

        self.add_button = QPushButton(
            "➕ Добавить"
        )

        self.remove_button = QPushButton(
            "➖ Удалить"
        )

        buttons.addWidget(
            self.add_button
        )

        buttons.addWidget(
            self.remove_button
        )

        buttons.addStretch()

        self.build_button = QPushButton(
            "📄 Сформировать сводку"
        )

        buttons.addWidget(
            self.build_button
        )

        layout.addLayout(
            buttons
        )

        root.addWidget(
            group
        )

        self.date.dateChanged.connect(
            self.on_date_changed
        )

        self.add_button.clicked.connect(
            self.on_add
        )

        self.remove_button.clicked.connect(
            self.on_remove
        )

        self.build_button.clicked.connect(
            self.on_build
        )

        self.update_buttons()
            # ---------------------------------------------------------

    def set_manager(
        self,
        manager,
    ):

        self.manager = manager

        self.on_date_changed()

    # ---------------------------------------------------------

    def update_buttons(self):

        enabled = self.manager is not None

        self.add_button.setEnabled(
            enabled
        )

        self.remove_button.setEnabled(
            enabled
        )

        self.build_button.setEnabled(
            enabled
        )
