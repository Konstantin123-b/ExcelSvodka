from core.models import Equipment


class EquipmentManager:
    """
    Поиск техники на листе Excel.
    """

    MODEL_COLUMN = 4
    GARAGE_COLUMN = 6

    def __init__(self, excel):
        self.excel = excel

    def find_first_row(self):

        for row in range(10, self.excel.rows + 1):

            model = self.excel.cell(row, self.MODEL_COLUMN)
            garage = self.excel.cell(row, self.GARAGE_COLUMN)

            if model and garage:
                return row

        raise RuntimeError(
            "Не удалось определить первую строку техники."
        )

    def find(self, garage_number: str, model: str | None = None):

        result = []

        start = self.find_first_row()

        for row in range(start, self.excel.rows + 1):

            garage = self.excel.cell(row, self.GARAGE_COLUMN)

            if str(garage).strip() != garage_number:
                continue

            current_model = str(
                self.excel.cell(row, self.MODEL_COLUMN)
            ).strip()

            if model is not None and current_model != model:
                continue

            result.append(
                Equipment(
                    row=row,
                    model=current_model,
                    garage_number=garage_number,
                )
            )

        return result