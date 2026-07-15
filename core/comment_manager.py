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
    employees,
) -> str:

    parts = []

    work = (work or "").strip()

    if work:
        parts.append("Работа:")
        parts.append(work)

    if isinstance(employees, str):
        employees = [
            x.strip()
            for x in employees.split(",")
            if x.strip()
        ]

    elif employees is None:
        employees = []

    if employees:

        if parts:
            parts.append("")

        parts.append("Исполнители:")
        parts.append(", ".join(employees))

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
