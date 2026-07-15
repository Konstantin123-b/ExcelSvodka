from __future__ import annotations

from copy import deepcopy

from core.comment_manager import CommentManager
from core.date_manager import DateManager
from core.equipment_manager import EquipmentManager
from core.models import MachineState
from core.models import SvodkaRecord
from core.svodka_loader import SvodkaLoader
from core.style_manager import StyleManager
from core.worksheet_editor import WorksheetEditor


class SvodkaManager:
    """
    Главное ядро ExcelSvodka 2.0

    Хранит список записей
    и формирует ежедневную сводку.
    """

    def __init__(self, excel):

        self.excel = excel

        self.loader = SvodkaLoader(excel)

        self.comments = CommentManager(excel)

        self.editor = WorksheetEditor(excel)

        self.equipment = EquipmentManager(excel)

        self.dates = DateManager(excel)

        self.records: list[SvodkaRecord] = []

    # ---------------------------------------------------------

    def clear(self):

        self.records.clear()

    # ---------------------------------------------------------

    def load_previous_day(
        self,
        date_string: str,
    ):

        self.records = self.loader.load_unique(
            date_string
        )

    # ---------------------------------------------------------

    def all(self):

        return deepcopy(
            self.records
        )

    # ---------------------------------------------------------

    def count(self):

        return len(
            self.records
        )

    # ---------------------------------------------------------

    def add(
        self,
        record: SvodkaRecord,
    ):

        garage = (
            record.garage_number
            .strip()
            .lower()
        )

        for item in self.records:

            if (
                item.garage_number
                .strip()
                .lower()
            ) == garage:

                raise RuntimeError(
                    f"Машина №{record.garage_number} уже присутствует в сводке."
                )

        self.records.append(record)

        self.sort()
          # ---------------------------------------------------------

    def remove(
        self,
        index: int,
    ):

        del self.records[index]

    # ---------------------------------------------------------

    def update(
        self,
        index: int,
        record: SvodkaRecord,
    ):

        garage = (
            record.garage_number
            .strip()
            .lower()
        )

        for i, item in enumerate(self.records):

            if i == index:
                continue

            if (
                item.garage_number
                .strip()
                .lower()
            ) == garage:

                raise RuntimeError(
                    f"Машина №{record.garage_number} уже присутствует в сводке."
                )

        self.records[index] = record

        self.sort()

    # ---------------------------------------------------------

    def sort(self):

        self.records.sort(
            key=lambda x: (
                x.model.lower(),
                x.garage_number.lower(),
            )
        )

    # ---------------------------------------------------------

    def unavailable_count(self):

        return len(self.records)

    # ---------------------------------------------------------

    def build(
        self,
        date_string: str,
    ):
        """
        Формирует выбранную дату в Excel.

        Алгоритм:

        1. Очищает выбранную дату.
        2. Записывает все записи из списка.
        """

        column = self.dates.find(
            date_string
        )

        self._clear_column(column)

        for record in self.records:

            equipment = self.equipment.find(
                garage_number=record.garage_number,
                model=record.model,
            )

            if not equipment:

                raise RuntimeError(
                    f"Не найдена техника {record.garage_number}"
                )

            machine = equipment[0]

            self._write_record(
                machine.row,
                column,
                record,
            )

        self.excel.save()
          # ---------------------------------------------------------

    def _clear_column(
        self,
        column: int,
    ):
        """
        Полностью очищает выбранную дату
        от записей сводки.
        """

        start_row = self.equipment.find_first_row()

        for row in range(
            start_row,
            self.excel.rows + 1,
        ):

            cell = self.excel.worksheet.cell(
                row=row,
                column=column,
            )

            value = str(
                cell.value or ""
            ).strip().lower()

            if value not in (
                MachineState.IDLE.value,
                MachineState.ACCIDENT.value,
                MachineState.PLANNED.value,
                MachineState.CUSTOMER.value,
            ):
                continue

            cell.value = ""

            cell.fill = StyleManager.get_fill("")

            cell.comment = None

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

        cell = self.excel.worksheet.cell(
            row=row,
            column=column,
        )

        cell.value = record.code

        cell.fill = StyleManager.get_fill(
    record.code
        )

        # Примечание.
        self.comments.set(
            row=row,
            column=column,
            record=record,
        )
          # ---------------------------------------------------------

    def find(
        self,
        garage_number: str,
    ) -> SvodkaRecord | None:

        garage = garage_number.strip().lower()

        for record in self.records:

            if (
                record.garage_number
                .strip()
                .lower()
            ) == garage:

                return record

        return None

    # ---------------------------------------------------------

    def find_index(
        self,
        garage_number: str,
    ) -> int:

        garage = garage_number.strip().lower()

        for index, record in enumerate(self.records):

            if (
                record.garage_number
                .strip()
                .lower()
            ) == garage:

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

        if index < 0:

            self.add(record)

            return

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

    def contains(
        self,
        garage_number: str,
    ) -> bool:

        return (
            self.find_index(
                garage_number
            ) >= 0
        )
