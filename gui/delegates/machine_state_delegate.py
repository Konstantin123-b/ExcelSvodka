from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QStyledItemDelegate,
)

from core.models import MachineState


class MachineStateDelegate(QStyledItemDelegate):

    STATES = (
        MachineState.IDLE,
        MachineState.ACCIDENT,
        MachineState.PLANNED,
        MachineState.CUSTOMER,
    )

    # ---------------------------------------------------------

    def createEditor(
        self,
        parent,
        option,
        index,
    ):

        combo = QComboBox(parent)

        for state in self.STATES:

            combo.addItem(
                state.title,
                state,
            )

        return combo

    # ---------------------------------------------------------

    def setEditorData(
        self,
        editor,
        index,
    ):

        value = index.model().data(
            index,
            Qt.EditRole,
        )

        for i in range(editor.count()):

            if editor.itemText(i) == value:

                editor.setCurrentIndex(i)

                return
                  # ---------------------------------------------------------

    def setModelData(
        self,
        editor,
        model,
        index,
    ):

        model.setData(
            index,
            editor.currentText(),
            Qt.EditRole,
        )

    # ---------------------------------------------------------

    def updateEditorGeometry(
        self,
        editor,
        option,
        index,
    ):

        editor.setGeometry(
            option.rect
        )
