from PySide6.QtWidgets import (
    QHeaderView,
    QTableView,
)

from gui.delegates.machine_state_delegate import MachineStateDelegate


class SvodkaTable(QTableView):
    """
    Таблица сводки.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build()

    # ---------------------------------------------------------

    def _build(self):

        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.setSelectionMode(
            QTableView.SingleSelection
        )

        self.setSortingEnabled(False)

        self.verticalHeader().setVisible(True)
        self.verticalHeader().setDefaultSectionSize(24)
        self.verticalHeader().setMinimumWidth(45)

        header = self.horizontalHeader()

        header.setStretchLastSection(False)

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.Stretch,
        )

        self.setItemDelegateForColumn(
            0,
            MachineStateDelegate(self),
        )

    # ---------------------------------------------------------

    def selected_row(self) -> int:

        indexes = self.selectionModel().selectedRows()

        if not indexes:
            return -1

        return indexes[0].row()