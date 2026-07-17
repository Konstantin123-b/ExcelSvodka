from copy import deepcopy

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

    STATE_NAMES = {
        MachineState.IDLE: "Простой",
        MachineState.ACCIDENT: "Аварийный ремонт",
        MachineState.PLANNED: "Плановые работы",
        MachineState.CUSTOMER: "Работы заказчика",
    }

    NAME_TO_STATE = {
        value: key
        for key, value in STATE_NAMES.items()
    }

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

        if role not in (
            Qt.DisplayRole,
            Qt.EditRole,
        ):
            return None

        match index.column():

            case 0:
                return self.STATE_NAMES.get(
                    record.state,
                    "",
                )

            case 1:
                return record.model

            case 2:
                return record.garage_number

            case 3:
                return record.description

            case 4:
                return record.operating_hours

            case 5:
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

        match index.column():

            case 0:

                state = self.NAME_TO_STATE.get(value)

                if state is None:
                    return False

                record.state = state

            case 3:
                record.description = value

            case 4:
                record.operating_hours = value

            case 5:
                record.employees = value

            case _:
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

        return deepcopy(self.records)