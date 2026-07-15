from __future__ import annotations

from datetime import datetime, timedelta

from core.models import MachineState, SvodkaRecord


class SvodkaLoader:
    """
    Загружает записи предыдущего дня из Excel.
    """

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

        records = self._remove_duplicates(
            records
        )

        return self._sort_records(
            records
        )
            # ---------------------------------------------------------

    @staticmethod
    def previous_day(
        date_string: str,
    ) -> str:
        """
        Возвращает предыдущую дату.
        """

        current = datetime.strptime(
            date_string,
            "%d.%m.%Y",
        )

        previous = current - timedelta(days=1)

        return previous.strftime(
            "%d.%m.%Y"
        )

    # ---------------------------------------------------------

    @staticmethod
    def _parse_comment(
        text: str,
    ) -> tuple[str, str, str]:
        """
        Разбирает комментарий Excel.

        Формат:

        Описание

        Наработка: 12345

        Иванов, Петров
        """

        text = text.replace(
            "\r\n",
            "\n",
        ).strip()

        if not text:
            return "", "", ""

        description = ""
        operating_hours = ""
        employees = ""

        blocks = [
            block.strip()
            for block in text.split("\n\n")
            if block.strip()
        ]

        for block in blocks:

            if block.startswith("Наработка:"):

                operating_hours = (
                    block.replace(
                        "Наработка:",
                        "",
                    ).strip()
                )

                continue

            if not description:

                description = block

            else:

                employees = block

        return (
            description,
            operating_hours,
            employees,
        )
            # ---------------------------------------------------------

    @staticmethod
    def _remove_duplicates(
        records: list[SvodkaRecord],
    ) -> list[SvodkaRecord]:
        """
        Удаляет дубликаты по гаражному номеру.
        Последняя запись имеет приоритет.
        """

        unique: dict[str, SvodkaRecord] = {}

        for record in records:

            key = record.garage_number.strip().lower()

            unique[key] = record

        return list(unique.values())

    # ---------------------------------------------------------

    @staticmethod
    def _sort_records(
        records: list[SvodkaRecord],
    ) -> list[SvodkaRecord]:
        """
        Сортирует записи по модели и
        гаражному номеру.
        """

        records.sort(

            key=lambda record: (

                record.model.lower(),

                record.garage_number.lower(),

            )
        )

        return records
            # ---------------------------------------------------------

    def load_unique(
        self,
        date_string: str,
    ) -> list[SvodkaRecord]:
        """
        Совместимость со старым SvodkaManager.
        """

        return self.load(
            date_string
        )
