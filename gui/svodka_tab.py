from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from gui.models.svodka_table_model import (
    SvodkaTableModel,
)

from gui.delegates.machine_state_delegate import (
    MachineStateDelegate,
)


class SvodkaTab(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.manager = None

        self.model = SvodkaTableModel(self)

        self._build_ui()

    # ---------------------------------------------------------

    def _build_ui(self):

        root = QVBoxLayout(self)

        group = QGroupBox(
            "Ежедневная сводка"
        )

        root.addWidget(group)

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

        self.info = QLabel()
        
        self.info.setWordWrap(True)
        
        self.info.setMinimumHeight(90)

        layout.addWidget(
            self.info
        )

        self.table = QTableView()

        self.table.setModel(
            self.model
        )
        from PySide6.QtWidgets import QHeaderView
        
        header = self.table.horizontalHeader()

        header.setStretchLastSection(True)

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch,
        )

        self.table.setItemDelegateForColumn(
            0,
            MachineStateDelegate(self.table),
        )
        
        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.verticalHeader().setVisible(True)

        self.table.verticalHeader().setDefaultSectionSize(24)

        self.table.verticalHeader().setMinimumWidth(45)

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

        self.update_buttons()

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

            self.model.set_records(
                self.manager.all()
            )

            filename = ""

            if getattr(self.manager.excel, "filename", ""):

                import os

                filename = os.path.basename(
                self.manager.excel.filename
                )

            total = len(
                list(
                    self.manager.excel.iter_equipment()
                )
            )

            self.info.setText(
                f"""Файл: {filename}

            Дата: {self.current_date()}

            Общее кол-во техники: {total}

            Общее кол-во техники в простое: {self.manager.count()}"""
            )

            self.table.resizeColumnsToContents()

            self.table.horizontalHeader().setStretchLastSection(
                True
            )

        except Exception as e:

            self.model.clear()

            self.info.setText(
                str(e)
            )
    # ---------------------------------------------------------

    def selected_row(self) -> int:

        indexes = self.table.selectionModel().selectedRows()

        if not indexes:
            return -1

        return indexes[0].row()

    # ---------------------------------------------------------

    def on_remove(self):

        if self.manager is None:
            return

        row = self.selected_row()

        if row < 0:
            return

        result = QMessageBox.question(
            self,
            "ExcelSvodka",
            "Удалить выбранную запись?",
        )

        if result != QMessageBox.Yes:
            return

        self.manager.remove(row)

        self.model.set_records(
            self.manager.all()
        )

    # ---------------------------------------------------------

    def on_build(self):

        if self.manager is None:
            return

        result = QMessageBox.question(
            self,
            "ExcelSvodka",
            (
                "Будет полностью сформирована "
                "сводка на выбранную дату.\n\n"
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

    def on_add(self):

        from gui.add_record_dialog import AddRecordDialog

        if self.manager is None:
            return

        dialog = AddRecordDialog(
            self.manager,
            self,
        )

        if not dialog.exec():
            return

        record = dialog.record()

        try:

            self.manager.add(record)

            self.model.set_records(
                self.manager.all()
            )

            self.table.resizeColumnsToContents()

            self.table.horizontalHeader().setStretchLastSection(
                True
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

        widths = (
            170,  # Тип
            170,  # Модель
            120,  # Гаражный №
            420,  # Описание
            140,  # Наработка
        )

        for column, width in enumerate(widths):

            self.table.setColumnWidth(
                column,
                width,
            )

    # ---------------------------------------------------------

    def refresh(self):
        """
        Полностью обновляет таблицу.
        """

        if self.manager is None:
            return

        self.model.set_records(
            self.manager.all()
        )

        self.table.resizeRowsToContents()

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

    # ---------------------------------------------------------

    def clear(self):

        self.model.clear()

        self.info.clear()

    # ---------------------------------------------------------

    def manager_ready(self) -> bool:

        return self.manager is not None
