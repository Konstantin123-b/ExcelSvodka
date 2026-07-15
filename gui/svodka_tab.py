from __future__ import annotations

from typing import List

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QDateEdit,
    QMessageBox,
)

from core.models import SvodkaRecord
from core.svodka_manager import SvodkaManager


class SvodkaTab(QWidget):
    """
    Основная вкладка ExcelSvodka 2.0.

    Единственный источник данных пользователя.
    Старые вкладки "Работы" и "Простои" больше не используются.
    """

    HEADERS = (
        "Тип",
        "Модель",
        "Гаражный №",
        "Описание",
        "Наработка",
        "Исполнители",
    )

    def __init__(self, excel_manager, equipment_manager, parent=None):
        super().__init__(parent)

        self.excel_manager = excel_manager
        self.equipment_manager = equipment_manager

        self.manager = SvodkaManager(
            excel_manager=self.excel_manager,
            equipment_manager=self.equipment_manager,
        )

        self.records: List[SvodkaRecord] = []

        self._build_ui()
        self._connect_signals()

        self.load_previous_day()
          def _build_ui(self):
        layout = QVBoxLayout(self)

        # -------------------------
        # Верхняя панель
        # -------------------------

        top = QHBoxLayout()

        top.addWidget(QLabel("Дата:"))

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        top.addWidget(self.date_edit)

        self.btn_load = QPushButton("Загрузить предыдущий день")
        self.btn_add = QPushButton("Добавить запись")
        self.btn_delete = QPushButton("Удалить запись")
        self.btn_generate = QPushButton("Сформировать сводку")

        top.addStretch()

        top.addWidget(self.btn_load)
        top.addWidget(self.btn_add)
        top.addWidget(self.btn_delete)
        top.addWidget(self.btn_generate)

        layout.addLayout(top)

        # -------------------------
        # Таблица
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()

        header.setStretchLastSection(False)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.Stretch,
        )

        layout.addWidget(self.table)
    def _connect_signals(self):
        self.btn_load.clicked.connect(
            self.load_previous_day
        )

        self.btn_add.clicked.connect(
            self.add_record
        )

        self.btn_delete.clicked.connect(
            self.delete_record
        )

        self.btn_generate.clicked.connect(
            self.generate_svodka
        )

        self.date_edit.dateChanged.connect(
            self.load_previous_day
        )
          # ---------------------------------------------------------
    # Работа с таблицей
    # ---------------------------------------------------------

    def add_record(self):
        """
        Добавить пустую запись.
        """
        record = SvodkaRecord(
            type="",
            model="",
            garage_number="",
            description="",
            hours="",
            workers="",
        )

        self.records.append(record)
        self.refresh_table()

        row = len(self.records) - 1
        self.table.selectRow(row)

    def delete_record(self):
        """
        Удалить выбранную запись.
        """

        row = self.table.currentRow()

        if row < 0:
            return

        del self.records[row]

        self.refresh_table()

    def refresh_table(self):
        """
        Перерисовать таблицу.
        """

        self.table.setRowCount(len(self.records))

        for row, record in enumerate(self.records):

            values = (
                record.type,
                record.model,
                record.garage_number,
                record.description,
                record.hours,
                record.workers,
            )

            for column, value in enumerate(values):

                item = QTableWidgetItem("" if value is None else str(value))
                item.setFlags(
                    item.flags() | Qt.ItemIsEditable
                )

                self.table.setItem(row, column, item)

    def collect_records(self):
        """
        Считать таблицу обратно в список SvodkaRecord.
        """

        self.records.clear()

        for row in range(self.table.rowCount()):

            self.records.append(
                SvodkaRecord(
                    type=self._text(row, 0),
                    model=self._text(row, 1),
                    garage_number=self._text(row, 2),
                    description=self._text(row, 3),
                    hours=self._text(row, 4),
                    workers=self._text(row, 5),
                )
            )

    def _text(self, row: int, column: int) -> str:

        item = self.table.item(row, column)

        if item is None:
            return ""

        return item.text().strip()
          # ---------------------------------------------------------
    # Загрузка предыдущего дня
    # ---------------------------------------------------------

    def load_previous_day(self):
        """
        Загружает записи предыдущего дня относительно выбранной даты.
        """

        try:
            date = self.date_edit.date().toPython()

            self.records = self.manager.load_previous_day(date)

            self.refresh_table()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить предыдущий день.\n\n{e}",
            )

    # ---------------------------------------------------------
    # Формирование сводки
    # ---------------------------------------------------------

    def generate_svodka(self):
        """
        Полностью перезаписывает выбранную дату.
        """

        try:

            self.collect_records()

            date = self.date_edit.date().toPython()

            self.manager.save_day(
                date=date,
                records=self.records,
            )

            QMessageBox.information(
                self,
                "Готово",
                "Сводка успешно сформирована.",
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сформировать сводку.\n\n{e}",
            )

    # ---------------------------------------------------------
    # Обновление списка записей
    # ---------------------------------------------------------

    def set_records(self, records):
        self.records = list(records)
        self.refresh_table()

    def clear(self):
        self.records.clear()
        self.refresh_table()
          # ---------------------------------------------------------
    # Служебные методы
    # ---------------------------------------------------------

    def current_record(self):
        """
        Возвращает выбранную запись.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        self.collect_records()

        if row >= len(self.records):
            return None

        return self.records[row]

    def has_records(self) -> bool:
        return len(self.records) > 0

    def record_count(self) -> int:
        return len(self.records)

    def update_record(self, row: int, record: SvodkaRecord):
        """
        Замена записи с обновлением таблицы.
        """

        if row < 0:
            return

        if row >= len(self.records):
            return

        self.records[row] = record
        self.refresh_table()

    def append_records(self, records):
        """
        Добавить несколько записей.
        """

        self.records.extend(records)
        self.refresh_table()

    def selected_row(self):
        return self.table.currentRow()

    def select_last_row(self):

        if self.table.rowCount() == 0:
            return

        self.table.selectRow(
            self.table.rowCount() - 1
        )

    def resize_columns(self):

        header = self.table.horizontalHeader()

        header.resizeSections(
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.Stretch,
        )
