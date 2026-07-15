from core.change_manager import ChangeManager
from core.comment_manager import CommentManager
from core.date_manager import DateManager
from core.equipment_manager import EquipmentManager
from core.idle_transfer_manager import IdleTransferManager
from core.models import Change
from core.worksheet_editor import WorksheetEditor


class SvodkaEngine:

    def __init__(self, excel):

        self.excel = excel

        self.dates = DateManager(excel)

        self.equipment = EquipmentManager(excel)

        self.comments = CommentManager(excel)

        self.editor = WorksheetEditor(excel)

        self.idle = IdleTransferManager(
            excel,
            self.dates,
        )

        self.changes = ChangeManager()

    def add_work(
        self,
        garage_number,
        model,
        date,
        code,
        work,
        employees,
    ):

        self.changes.add(
            Change(
                garage_number=garage_number,
                model=model,
                date=date,
                code=code,
                work=work,
                employees=employees,
            )
        )

    def apply_changes(self):

        for change in self.changes.all():

            cell_code = ">" if str(change.code).strip() == ">" else ""

            row, column = self.editor.write_code(
                garage_number=change.garage_number,
                model=change.model,
                date=change.date,
                code=cell_code,
            )

            self.comments.set(
                row=row,
                column=column,
                work=change.work,
                employees=change.employees,
            )

        self.changes.clear()

    def list_changes(self):

        return self.changes.all()

    def transfer_idle(self, date):

        return self.idle.transfer_all(date)

    def save(self):

        self.excel.save()
