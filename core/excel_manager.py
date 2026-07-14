from pathlib import Path

from openpyxl import load_workbook
from core.models import Equipment
from datetime import datetime


class ExcelManager:
    """
    Работа с книгой Excel.
    """

    TARGET_SHEET = "График по работам"

    def __init__(self):
        self.filename = ""
        self.workbook = None
        self.worksheet = None

    def open(self, filename: str):
        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(
                f"Файл не найден:\n{filename}"
            )

        self.filename = str(path)

        self.workbook = load_workbook(
            filename=self.filename,
            data_only=False,
        )

        if self.TARGET_SHEET not in self.workbook.sheetnames:
            raise RuntimeError(
                f"Лист '{self.TARGET_SHEET}' отсутствует."
            )

        self.worksheet = self.workbook[self.TARGET_SHEET]

    def close(self):
        self.workbook = None
        self.worksheet = None

    @property
    def opened(self):
        return self.workbook is not None

    @property
    def rows(self):
        return self.worksheet.max_row

    @property
    def columns(self):
        return self.worksheet.max_column

    def cell(self, row: int, column: int):
        """
        Возвращает значение ячейки.
        """
        return self.worksheet.cell(
            row=row,
            column=column,
        ).value

    def find_first_row(self):
        """
        Находит первую строку техники.
        D = модель
        F = гаражный номер
        """
        for row in range(1, self.rows + 1):

            model = self.cell(row, 4)
            garage = self.cell(row, 6)

            if model and garage:
                return row

        raise RuntimeError(
            "Не удалось определить первую строку техники."
        )

    def find_by_garage_number(self, garage_number: str):
        """
        Возвращает список строк,
        соответствующих гаражному номеру.
        """

        result = []

        start_row = self.find_first_row()

        for row in range(start_row, self.rows + 1):

            value = self.cell(row, 6)

            if value is None:
                continue

            if str(value).strip() == str(garage_number).strip():
                result.append(row)

        return result  
    def get_equipment(self, garage_number: str):
        """
        Возвращает найденную технику.
        """

        rows = self.find_by_garage_number(garage_number)

        equipment = []

        for row in rows:

            equipment.append(
                Equipment(
                    row=row,
                    model=str(self.cell(row, 4)),
                    garage_number=str(self.cell(row, 6)),
                )
            )

        return equipment
    from datetime import datetime

    def find_date_column(self, date_string: str):
        """
        Возвращает номер столбца для указанной даты.
        """

        target = datetime.strptime(
            date_string,
            "%d.%m.%Y"
        ).date()

        # В вашей книге даты находятся в 9-й строке.
        for column in range(1, self.columns + 1):

            value = self.cell(9, column)

            if hasattr(value, "date"):

                if value.date() == target:
                    return column

        raise RuntimeError(
            f"Дата {date_string} не найдена."
        )
    def find_target_cell(self, garage_number: str, date_string: str):
        """
        Возвращает координаты нужной ячейки.
        """

        rows = self.find_by_garage_number(garage_number)

        if not rows:
            raise RuntimeError(
                f"Техника №{garage_number} не найдена."
            )

        if len(rows) > 1:
            raise RuntimeError(
                "Найдено несколько машин с таким гаражным номером."
            )

        column = self.find_date_column(date_string)

        return rows[0], column 
    def set_cell(self, row: int, column: int, value):
        """
        Записывает значение в ячейку.
        """
        self.worksheet.cell(
            row=row,
            column=column
        ).value = value

    def save(self, filename: str | None = None):
        """
        Сохраняет книгу.
        """

        if filename is None:
            filename = self.filename

        self.workbook.save(filename)
    def set_fill(self, row: int, column: int, fill):

        self.worksheet.cell(
            row=row,
            column=column
        ).fill = fill  
          