from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from core.models import (
    MachineState,
    SvodkaRecord,
)


class SvodkaLoader:
    """
    Загружает записи предыдущего дня
    из файла Excel.
    """

    def __init__(self, excel):

        self.excel = excel

    # ---------------------------------------------------------

    def load(
        self,
        date_string: str,
    ) -> list[SvodkaRecord]:

        previous = self._previous_day(
            date_string
        )

        column = self.excel.find_date_column(
            previous
        )

        if column is None:

            raise RuntimeError(
                f"Дата {previous} не найдена."
            )

        records = []

        for machine in self.excel.iter_equipment():

            cell = self.excel.worksheet.cell(
                row=machine.row,
                column=column,
            )

            code = str(
                cell.value or ""
            ).strip().lower()

            state = MachineState.from_code(
                code
            )

            if state is None:
                continue

            description = ""
            operating_hours = ""
            employees = ""
            
