from openpyxl.comments import Comment


class CommentManager:

    AUTHOR = "ExcelSvodka"

    def __init__(self, excel):
        self.excel = excel

    def get(self, row: int, column: int):

        cell = self.excel.worksheet.cell(
            row=row,
            column=column,
        )

        if cell.comment is None:
            return ""

        return cell.comment.text

    def build(
        self,
        work: str,
        employees: list[str],
    ) -> str:

        parts = []

        work = work.strip()

        if work:

            parts.append("Работа:")
            parts.append(work)

        employees = [
            x.strip()
            for x in employees
            if x.strip()
        ]

        if employees:

            if parts:
                parts.append("")

            parts.append("Исполнители:")

            parts.extend(employees)

        return "\n".join(parts)

    def set(
        self,
        row: int,
        column: int,
        work: str,
        employees: list[str],
    ):

        text = self.build(
            work,
            employees,
        )

        cell = self.excel.worksheet.cell(
            row=row,
            column=column,
        )

        if text:

            cell.comment = Comment(
                text=text,
                author=self.AUTHOR,
            )

        else:

            cell.comment = None