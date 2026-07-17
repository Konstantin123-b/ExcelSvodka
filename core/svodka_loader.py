from __future__ import annotations

from datetime import datetime, timedelta

from core.models import (
    MachineState,
    SvodkaRecord,
)

from core.color_detector import ColorDetector


class SvodkaLoader:

    def __init__(self, excel):

        self.excel = excel

    # ---------------------------------------------------------

    def load(
        self,
        date_string: str,
    ) -> list[SvodkaRecord]:

        previous_date = self.previous_day(
            date_string
        )

        column = self.excel.find_date_column(
            previous_date
        )

        records = []

        for equipment in self.excel.iter_equipment():

            cell = self.excel.worksheet.cell(
                row=equipment.row,
                column=column,
            )

            code = str(
                cell.value or ""
            ).strip().lower()

            # Если в ячейке нет символа,
            # пытаемся определить код по цвету.

            if not code:

                code = ColorDetector.detect(
                    cell.fill
                ) or ""

            state = MachineState.from_code(
                code
            )

            if state is None:
                continue
            description = ""
            operating_hours = ""
            employees = ""

            if cell.comment is not None:

                (
                    description,
                    operating_hours,
                    employees,
                ) = self._parse_comment(
                    cell.comment.text
                )

            records.append(

                SvodkaRecord(

                    state=state,

                    garage_number=equipment.garage_number,

                    model=equipment.model,

                    description=description,

                    operating_hours=operating_hours,

                    employees=employees,

                )

            )

        print("===== LOADED =====")
        for r in records:
            print(type(r.state), repr(r.state))

        return self._sort_records(

            self._remove_duplicates(
                records
            )

        )

    # ---------------------------------------------------------

    @staticmethod
    def previous_day(
        date_string: str,
    ) -> str:

        current = datetime.strptime(
            date_string,
            "%d.%m.%Y",
        )

        previous = current - timedelta(
            days=1
        )

        return previous.strftime(
            "%d.%m.%Y"
        )
    # ---------------------------------------------------------

    @staticmethod
    def _parse_comment(
        text: str,
    ) -> tuple[str, str, str]:

        description = ""
        operating_hours = ""
        employees = ""

        if not text:
            return (
                description,
                operating_hours,
                employees,
            )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if len(lines) >= 1:
            description = lines[0]

        if len(lines) >= 2:
            operating_hours = lines[1]

        if len(lines) >= 3:
            employees = "\n".join(
                lines[2:]
            )

        return (
            description,
            operating_hours,
            employees,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _sort_records(
        records,
    ):

        return sorted(
            records,
            key=lambda r: (
                r.state,
                r.model,
                r.garage_number,
            ),
        )
    # ---------------------------------------------------------

    @staticmethod
    def _remove_duplicates(
        records,
    ):

        result = []

        seen = set()

        for record in records:

            key = (
                record.garage_number,
                record.state,
            )

            if key in seen:
                continue

            seen.add(key)

            result.append(record)

        return result
