from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
)

from core.models import (
    MachineState,
    SvodkaRecord,
)


class SvodkaTableModel(QAbstractTableModel):

    HEADERS = (
        "Тип",
        "Модель",
        "Гаражный №",
        "Описание",
        "Наработка",
        "Исполнители",
    )

    def __init__(self, parent=None):

        super().__init__(parent)

        self.records: list[SvodkaRecord] = []

    # ---------------------------------------------------------

    def set_records(
        self,
        records: list[SvodkaRecord],
    ):

        self.beginResetModel()

        self.records = records

        self.endResetModel()

    # ---------------------------------------------------------

    def rowCount(
        self,
        parent=QModelIndex(),
    ):

        return len(self.records)

    # ---------------------------------------------------------

    def columnCount(
        self,
        parent=QModelIndex(),
    ):

        return len(self.HEADERS)

    # ---------------------------------------------------------

    def headerData(
        self,
        section,
        orientation,
        role,
    ):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return section + 1
          # ---------------------------------------------------------

    def data(
        self,
        index,
        role,
    ):

        if not index.isValid():
            return None

        record = self.records[index.row()]

        if role in (
            Qt.DisplayRole,
            Qt.EditRole,
        ):

            column = index.column()

            if column == 0:
                return record.state.title

            if column == 1:
                return record.model

            if column == 2:
                return record.garage_number

            if column == 3:
                return record.description

            if column == 4:
                return record.operating_hours

            if column == 5:
                return record.employees

        return None

    # ---------------------------------------------------------

    def flags(
        self,
        index,
    ):

        if not index.isValid():
            return Qt.NoItemFlags

        flags = (
            Qt.ItemIsEnabled
            | Qt.ItemIsSelectable
        )

        # Тип, описание, наработка и исполнители
        # можно редактировать.
        if index.column() in (
            0,
            3,
            4,
            5,
        ):
            flags |= Qt.ItemIsEditable

        return flags
          # ---------------------------------------------------------

    def setData(
        self,
        index,
        value,
        role,
    ):

        if role != Qt.EditRole:
            return False

        if not index.isValid():
            return False

        record = self.records[index.row()]

        value = str(value).strip()

        column = index.column()

        if column == 0:

            mapping = {
                "Простой": MachineState.IDLE,
                "Аварийный ремонт": MachineState.ACCIDENT,
                "Плановые работы": MachineState.PLANNED,
                "Работы заказчика": MachineState.CUSTOMER,
            }

            if value not in mapping:
                return False

            record.state = mapping[value]

        elif column == 3:

            record.description = value

        elif column == 4:

            record.operating_hours = value

        elif column == 5:

            record.employees = value

        else:

            return False

        self.dataChanged.emit(
            index,
            index,
            [
                Qt.DisplayRole,
                Qt.EditRole,
            ],
        )

        return True

    # ---------------------------------------------------------

    def record(
        self,
        row: int,
    ) -> SvodkaRecord:

        return self.records[row]
          # ---------------------------------------------------------

    def add_record(
        self,
        record: SvodkaRecord,
    ):

        row = len(self.records)

        self.beginInsertRows(
            QModelIndex(),
            row,
            row,
        )

        self.records.append(record)

        self.endInsertRows()

    # ---------------------------------------------------------

    def remove_record(
        self,
        row: int,
    ):

        if row < 0 or row >= len(self.records):
            return

        self.beginRemoveRows(
            QModelIndex(),
            row,
            row,
        )

        del self.records[row]

        self.endRemoveRows()

    # ---------------------------------------------------------

    def clear(self):

        self.beginResetModel()

        self.records.clear()

        self.endResetModel()

    # ---------------------------------------------------------

    def all_records(
        self,
    ) -> list[SvodkaRecord]:

        return self.records
