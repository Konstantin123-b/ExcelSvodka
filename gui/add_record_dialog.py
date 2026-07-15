from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from core.models import (
    MachineState,
    SvodkaRecord,
)


class AddRecordDialog(QDialog):

    def __init__(
        self,
        manager,
        parent=None,
    ):

        super().__init__(parent)

        self.manager = manager

        self.setWindowTitle(
            "Добавить запись"
        )

        self.resize(550, 420)

        self._build_ui()
          # ---------------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.state = QComboBox()

        self.state.addItem(
            "Простой",
            MachineState.IDLE,
        )

        self.state.addItem(
            "Аварийный ремонт",
            MachineState.ACCIDENT,
        )

        self.state.addItem(
            "Плановые работы",
            MachineState.PLANNED,
        )

        self.state.addItem(
            "Работы заказчика",
            MachineState.CUSTOMER,
        )

        form.addRow(
            "Тип",
            self.state,
        )

        self.garage = QLineEdit()

        form.addRow(
            "Гаражный №",
            self.garage,
        )

        self.model = QLabel("-")

        form.addRow(
            "Модель",
            self.model,
        )

        self.description = QTextEdit()

        self.description.setMaximumHeight(
            80
        )

        form.addRow(
            "Описание",
            self.description,
        )

        self.operating_hours = QLineEdit()

        form.addRow(
            "Наработка",
            self.operating_hours,
        )

        self.employees = QTextEdit()

        self.employees.setMaximumHeight(
            70
        )

        form.addRow(
            "Исполнители",
            self.employees,
        )

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            |
            QDialogButtonBox.Cancel
        )

        layout.addWidget(
            self.buttons
        )

        self.buttons.accepted.connect(
            self.accept
        )

        self.buttons.rejected.connect(
            self.reject
        )

        self.garage.textChanged.connect(
            self.on_garage_changed
        )
          # ---------------------------------------------------------

    def on_garage_changed(self):

        garage = self.garage.text().strip()

        self.model.setText("-")

        if not garage:
            return

        try:

            machines = self.manager.equipment.find(
                garage_number=garage,
                model=None,
            )

        except Exception:
            return

        if not machines:
            return

        self.model.setText(
            machines[0].model
        )

    # ---------------------------------------------------------

    def accept(self):

        garage = self.garage.text().strip()

        if not garage:

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                "Введите гаражный номер.",
            )

            return

        if self.model.text() == "-":

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                "Машина не найдена.",
            )

            return

        super().accept()
          # ---------------------------------------------------------

    def record(self) -> SvodkaRecord:

        return SvodkaRecord(

            state=self.state.currentData(),

            garage_number=self.garage.text().strip(),

            model=self.model.text().strip(),

            description=self.description.toPlainText().strip(),

            operating_hours=self.operating_hours.text().strip(),

            employees=self.employees.toPlainText().strip(),
        )

    # ---------------------------------------------------------

    def clear(self):

        self.state.setCurrentIndex(0)

        self.garage.clear()

        self.model.setText("-")

        self.description.clear()

        self.operating_hours.clear()

        self.employees.clear()

    # ---------------------------------------------------------

    def set_record(
        self,
        record: SvodkaRecord,
    ):
        """
        Понадобится позже
        для редактирования записи.
        """

        mapping = {
            MachineState.IDLE: 0,
            MachineState.ACCIDENT: 1,
            MachineState.PLANNED: 2,
            MachineState.CUSTOMER: 3,
        }

        self.state.setCurrentIndex(
            mapping[record.state]
        )

        self.garage.setText(
            record.garage_number
        )

        self.model.setText(
            record.model
        )

        self.description.setPlainText(
            record.description
        )

        self.operating_hours.setText(
            record.operating_hours
        )

        self.employees.setPlainText(
            record.employees
        )
          # ---------------------------------------------------------

    def selected_state(self) -> MachineState:

        return self.state.currentData()

    # ---------------------------------------------------------

    def garage_number(self) -> str:

        return self.garage.text().strip()

    # ---------------------------------------------------------

    def model_name(self) -> str:

        return self.model.text().strip()

    # ---------------------------------------------------------

    def description_text(self) -> str:

        return self.description.toPlainText().strip()

    # ---------------------------------------------------------

    def operating_hours_text(self) -> str:

        return self.operating_hours.text().strip()

    # ---------------------------------------------------------

    def employees_text(self) -> str:

        return self.employees.toPlainText().strip()

    # ---------------------------------------------------------

    def validate(self) -> tuple[bool, str]:

        if not self.garage_number():
            return False, "Введите гаражный номер."

        if self.model_name() in ("", "-"):
            return False, "Не удалось определить модель."

        if not self.description_text():
            return False, "Введите описание."

        return True, ""

    # ---------------------------------------------------------

    def accept(self):

        ok, message = self.validate()

        if not ok:

            QMessageBox.warning(
                self,
                "ExcelSvodka",
                message,
            )

            return

        super().accept()
