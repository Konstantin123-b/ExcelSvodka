from datetime import datetime


class DateManager:
    """
    Поиск столбца по дате.
    """

    DATE_ROW = 9

    def __init__(self, excel):
        self.excel = excel

    def find(self, date_string: str):

        target = datetime.strptime(
            date_string,
            "%d.%m.%Y"
        ).date()

        for column in range(1, self.excel.columns + 1):

            value = self.excel.cell(
                self.DATE_ROW,
                column,
            )

            if value is None:
                continue

            if hasattr(value, "date"):

                if value.date() == target:
                    return column

        raise RuntimeError(
            f"Дата {date_string} не найдена."
        )
