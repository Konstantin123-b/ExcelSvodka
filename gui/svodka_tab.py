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
            # ---------------------------------------------------------

    def current_date(self) -> str:

        return self.date.date().toString(
            "dd.MM.yyyy"
        )

    # ---------------------------------------------------------

    def on_date_changed(self):

        if self.manager is None:
            return

        try:

            self.manager.load_previous_day(
                self.current_date()
            )

            self.info.setText(
                f"Автоматически загружены записи за предыдущий день."
            )

            self.refresh()

        except Exception as e:

            self.info.setText(
                str(e)
            )

            self.table.setRowCount(0)

    # ---------------------------------------------------------

    def refresh(self):

        records = self.manager.all()

        self.table.setRowCount(
            len(records)
        )

        for row, record in enumerate(records):

            values = [

                record.state_name,

                record.model,

                record.garage_number,

                record.description,

                record.operating_hours,

                record.employees,

            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                # Модель и гаражный номер
                # запрещаем редактировать.

                if column in (1, 2):

                    item.setFlags(
                        item.flags()
                        & ~Qt.ItemIsEditable
                    )

                self.table.setItem(
                    row,
                    column,
                    item,
                )
                    # ---------------------------------------------------------

    def on_add(self):

        from PySide6.QtWidgets import QMessageBox

        QMessageBox.information(
            self,
            "ExcelSvodka",
            "Окно добавления записи будет подключено следующим этапом.",
        )

    # ---------------------------------------------------------

    def on_remove(self):

        if self.manager is None:
            return

        row = self.table.currentRow()

        if row < 0:
            return

        self.manager.remove(row)

        self.refresh()

    # ---------------------------------------------------------

    def on_build(self):

        if self.manager is None:
            return

        from PySide6.QtWidgets import QMessageBox

        result = QMessageBox.question(
            self,
            "ExcelSvodka",
            (
                "Будет полностью сформирована сводка "
                "на выбранную дату.\n\n"
                "Продолжить?"
            ),
        )

        if result != QMessageBox.Yes:
            return

        try:

            self.manager.build(
                self.current_date()
            )

            QMessageBox.information(
                self,
                "ExcelSvodka",
                "Сводка успешно сформирована.",
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e),
            )
                # ---------------------------------------------------------

    def resizeEvent(self, event):

        super().resizeEvent(event)

        header = self.table.horizontalHeader()

        header.setStretchLastSection(True)

        self.table.setColumnWidth(0, 170)  # Тип
        self.table.setColumnWidth(1, 170)  # Модель
        self.table.setColumnWidth(2, 120)  # Гаражный
        self.table.setColumnWidth(3, 420)  # Описание
        self.table.setColumnWidth(4, 140)  # Наработка
