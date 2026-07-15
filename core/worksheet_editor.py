from core.comment_manager import CommentManager
from core.date_manager import DateManager
from core.equipment_manager import EquipmentManager
from core.style_manager import StyleManager


class WorksheetEditor:
    """
    Изменение данных на листе Excel.
    """

    def __init__(self, excel):

        self.excel = excel

        self.equipment = EquipmentManager(excel)

        self.dates = DateManager(excel)

        self.comments = CommentManager(excel)

    def write_code(
        self,
        garage_number: str,
        model: str,
        date,
        code: str,
    ):

        machines = self.equipment.find(
            garage_number=garage_number,
            model=model,
        )

        if len(machines) != 1:
            raise RuntimeError(
                f"Найдено машин: {len(machines)}"
            )

        machine = machines[0]

        column = self.dates.find(date)

        cell = self.excel.worksheet.cell(
            row=machine.row,
            column=column,
        )

        value = str(code).strip().lower()

        # В ячейке оставляем только ">".
        # Все остальные обозначения ("ав", "з", "пл" и т.д.)
        # хранятся только в примечании.

        if value == ">":
            cell.value = ">"
            cell.fill = StyleManager.get_fill(value)
        else:
            cell.value = ""
            cell.fill = StyleManager.get_fill("")

        return machine.row, column

    def write_note(
        self,
        garage_number,
        model,
        date,
        work,
        employees,
    ):

        machines = self.equipment.find(
            garage_number=garage_number,
            model=model,
        )

        if len(machines) != 1:
            raise RuntimeError(
                f"Найдено машин: {len(machines)}"
            )

        machine = machines[0]

        column = self.dates.find(date)

        self.comments.set(
            row=machine.row,
            column=column,
            work=work,
            employees=employees,
        )

        return machine.row, column
