from datetime import datetime, timedelta

from core.equipment_manager import EquipmentManager


class IdleTransferManager:

    IDLE_MARK = ">"

    def __init__(self, excel, dates):
        self.excel = excel
        self.dates = dates
        self.equipment = EquipmentManager(excel)

    def next_date(self, date_string: str):

        date = datetime.strptime(
            date_string,
            "%d.%m.%Y"
        )

        return (
            date + timedelta(days=1)
        ).strftime("%d.%m.%Y")

    def transfer_row(self, row: int, date_string: str):

        today_column = self.dates.find(date_string)
        tomorrow_column = self.dates.find(
            self.next_date(date_string)
        )

        today = self.excel.cell(row, today_column)
        tomorrow = self.excel.cell(row, tomorrow_column)

        if today != self.IDLE_MARK:
            return False

        if tomorrow not in (None, ""):
            return False

        self.excel.set_cell(
            row,
            tomorrow_column,
            self.IDLE_MARK,
        )

        return True

    def transfer_all(self, date_string: str):

        transferred = []

        start = self.equipment.find_first_row()

        for row in range(start, self.excel.rows + 1):

            if self.transfer_row(row, date_string):

                transferred.append(
                    {
                        "row": row,
                        "model": self.excel.cell(row, 4),
                        "garage": self.excel.cell(row, 6),
                    }
                )

        return transferred