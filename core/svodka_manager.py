from __future__ import annotations

from copy import deepcopy

from core.comment_manager import CommentManager
from core.models import SvodkaRecord
from core.style_manager import StyleManager
from core.svodka_loader import SvodkaLoader


class SvodkaManager:
    """
    Главное ядро ExcelSvodka 2.0.

    Хранит список записей
    и формирует сводку.
    """

    def __init__(self, excel):

        self.excel = excel

        self.loader = SvodkaLoader(excel)

        self.comments = CommentManager(excel)

        self.records: list[SvodkaRecord] = []
            # ---------------------------------------------------------

    def clear(self):

        self.records.clear()

    # ---------------------------------------------------------

    def all(self) -> list[SvodkaRecord]:

        return deepcopy(
            self.records
        )

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(
            self.records
        )

    # ---------------------------------------------------------

    def sort(self):

        self.records.sort(
            key=lambda record: (
                record.model.lower(),
                record.garage_number.lower(),
            )
        )

    # ---------------------------------------------------------

    def load_previous_day(
        self,
        date_string: str,
    ):

        self.records = self.loader.load(
            date_string
        )

        self.sort()
            # ---------------------------------------------------------

    def add(
        self,
        record: SvodkaRecord,
    ):

        if self.contains(
            record.garage_number
        ):

            raise RuntimeError(
                f"Машина №{record.garage_number} уже есть в списке."
            )

        self.records.append(
            record
        )

        self.sort()

    # ---------------------------------------------------------

    def update(
        self,
        index: int,
        record: SvodkaRecord,
    ):

        for i, item in enumerate(self.records):

            if i == index:
                continue

            if (
                item.garage_number.strip().lower()
                ==
                record.garage_number.strip().lower()
            ):

                raise RuntimeError(
                    f"Машина №{record.garage_number} уже есть в списке."
                )

        self.records[index] = record

        self.sort()

    # ---------------------------------------------------------

    def remove(
        self,
        index: int,
    ):

        del self.records[index]

    # ---------------------------------------------------------

    def contains(
        self,
        garage_number: str,
    ) -> bool:

        garage_number = garage_number.strip().lower()

        return any(

            record.garage_number.strip().lower()
            ==
            garage_number

            for record in self.records

        )
            # ---------------------------------------------------------

    def build(
        self,
        date_string: str,
    ):
        """
        Полностью формирует выбранную дату.
        """

        column = self.excel.find_date_column(
            date_string
        )

        self._clear_column(
            column
        )

        for i, record in enumerate(self.records):
            print(i, type(record.state), repr(record.state))
        
        for record in self.records:

            equipment = self.excel.get_equipment(
                record.garage_number
            )

            self._write_record(

                row=equipment.row,

                column=column,

                record=record,

            )

        self.excel.save()

    # ---------------------------------------------------------

    def _clear_column(
        self,
        column: int,
    ):
        """
        Удаляет все записи сводки
        из выбранного дня.
        """

        from openpyxl.styles import PatternFill

        empty_fill = PatternFill(
            fill_type=None
        )

        for equipment in self.excel.iter_equipment():

            self.excel.set_cell(
                equipment.row,
                column,
                "",
            )

            self.excel.set_fill(
                equipment.row,
                column,
                empty_fill,
            )

            self.excel.clear_comment(
                equipment.row,
                column,
            )
                # ---------------------------------------------------------

    def _write_record(
        self,
        row: int,
        column: int,
        record: SvodkaRecord,
    ):
        """
        Записывает одну запись в Excel.
        """

        # Код состояния
        self.excel.set_cell(
            row,
            column,
            record.code,
        )

        # Цвет ячейки
        self.excel.set_fill(
            row,
            column,
            StyleManager.get_fill(
                record.code
            ),
        )

        # Комментарий
        comment = self.comments.build(
            record
        )

        self.excel.set_comment(
            row,
            column,
            comment,
        )
            # ---------------------------------------------------------

    def find(
        self,
        garage_number: str,
    ) -> SvodkaRecord | None:

        garage_number = garage_number.strip().lower()

        for record in self.records:

            if (
                record.garage_number.strip().lower()
                ==
                garage_number
            ):

                return record

        return None

    # ---------------------------------------------------------

    def find_index(
        self,
        garage_number: str,
    ) -> int:

        garage_number = garage_number.strip().lower()

        for index, record in enumerate(self.records):

            if (
                record.garage_number.strip().lower()
                ==
                garage_number
            ):

                return index

        return -1

    # ---------------------------------------------------------

    def replace(
        self,
        garage_number: str,
        record: SvodkaRecord,
    ):

        index = self.find_index(
            garage_number
        )

        if index == -1:

            self.add(record)

        else:

            self.update(
                index,
                record,
            )

    # ---------------------------------------------------------

    def remove_by_garage(
        self,
        garage_number: str,
    ):

        index = self.find_index(
            garage_number
        )

        if index >= 0:

            self.remove(index)

    # ---------------------------------------------------------

    def unavailable_count(self) -> int:
        """
        Количество недоступной техники.
        Сейчас все записи считаются недоступными.
        """

        return len(self.records)
