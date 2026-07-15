from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QStyledItemDelegate,
)

from core.models import MachineState


class MachineStateDelegate(QStyledItemDelegate):

    ITEMS = (
        ("Простой", MachineState.IDLE),
        ("Аварийный ремонт", MachineState.ACCIDENT),
        ("Плановые работы", MachineState.PLANNED),
        ("Работы заказчика", MachineState.CUSTOMER),
    )

    def createEditor(
        self,
        parent,
        option,
        index,
    ):

        combo = QComboBox(parent)

        for text, _ in self.ITEMS:
            combo.addItem(text)

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

        for i, (text, _) in enumerate(self.ITEMS):

            if text == value:

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