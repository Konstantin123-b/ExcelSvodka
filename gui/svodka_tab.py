from pathlib import Path

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from gui.add_record_dialog import AddRecordDialog
from gui.models.svodka_table_model import SvodkaTableModel
from gui.widgets.date_selector import DateSelector
from gui.widgets.info_panel import InfoPanel
from gui.widgets.svodka_table import SvodkaTable
from gui.widgets.svodka_toolbar import SvodkaToolbar


class SvodkaTab(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.manager = None

        self.model = SvodkaTableModel()

        self._build_ui()

    # ---------------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        self.info_panel = InfoPanel()

        layout.addWidget(self.info_panel)

        self.date_selector = DateSelector()

        layout.addWidget(self.date_selector)

        self.table = SvodkaTable()

        self.table.setModel(
            self.model
        )

        layout.addWidget(
            self.table,
            1,
        )

        self.toolbar = SvodkaToolbar()

        layout.addWidget(
            self.toolbar,
        )

        self.toolbar.add_clicked.connect(
            self.on_add
        )

        self.toolbar.remove_clicked.connect(
            self.on_remove
        )

        self.toolbar.build_clicked.connect(
            self.on_build
        )

        self.date_selector.date_changed.connect(
            self.on_date_changed
        )
            # ---------------------------------------------------------

    def set_manager(
        self,
        manager,
    ):

        self.manager = manager

        self.refresh()

    # ---------------------------------------------------------

    def current_date(self) -> str:

        return self.date_selector.date_string()

    # ---------------------------------------------------------

    def refresh(self):

        if self.manager is None:
            return

        self.model.set_records(
            self.manager.all()
        )

        if self.model.rowCount():

            self.table.selectRow(0)

        filename = ""

        if getattr(
            self.manager.excel,
            "filename",
            "",
        ):

            filename = Path(
                self.manager.excel.filename
            ).name

        total = len(
            list(
                self.manager.excel.iter_equipment()
            )
        )

        self.info_panel.update_info(
            filename=filename,
            date=self.current_date(),
            total=total,
            idle=self.manager.count(),
        )

    # ---------------------------------------------------------

    def on_date_changed(
        self,
        _,
    ):

        if self.manager is None:
            return

        try:

            self.manager.load_previous_day(
                self.current_date()
            )

            self.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )
                # ---------------------------------------------------------

    def on_add(self):

        if self.manager is None:
            return

        dialog = AddRecordDialog(
            self.manager,
            self,
        )

        if not dialog.exec():
            return

        try:

            self.manager.add(
                dialog.record()
            )

            self.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )

    # ---------------------------------------------------------

    def on_remove(self):

        if self.manager is None:
            return

        row = self.table.selected_row()

        if row < 0:
            return

        record = self.model.record(row)

        try:

            self.manager.remove_by_garage(
                record.garage_number
            )

            self.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )
                # ---------------------------------------------------------

    def on_build(self):

        if self.manager is None:
            return

        try:

            self.manager.build(
                self.current_date()
            )

            QMessageBox.information(
                self,
                "ExcelSvodka",
                "Сводка успешно сформирована.",
            )

            self.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )

    # ---------------------------------------------------------

    def selected_record(self):

        row = self.table.selected_row()

        if row < 0:
            return None

        return self.model.record(row)

    # ---------------------------------------------------------

    def clear(self):

        self.model.clear()

        self.info_panel.update_info(
            filename="-",
            date=self.current_date(),
            total=0,
            idle=0,
        )
            # ---------------------------------------------------------

    def on_build(self):

        if self.manager is None:
            return

        try:

            self.manager.build(
                self.current_date()
            )

            QMessageBox.information(
                self,
                "ExcelSvodka",
                "Сводка успешно сформирована.",
            )

            self.refresh()

        except Exception as e:

            QMessageBox.critical(
                self,
                "ExcelSvodka",
                str(e),
            )

    # ---------------------------------------------------------

    def selected_record(self):

        row = self.table.selected_row()

        if row < 0:
            return None

        return self.model.record(row)

    # ---------------------------------------------------------

    def clear(self):

        self.model.clear()

        self.info_panel.update_info(
            filename="-",
            date=self.current_date(),
            total=0,
            idle=0,
        )
            # ---------------------------------------------------------

    def connect_signals(self):

        self.table.doubleClicked.connect(
            lambda _: self.on_edit()
        )

    # ---------------------------------------------------------

    def set_enabled(
        self,
        enabled: bool,
    ):

        self.date_selector.setEnabled(
            enabled
        )

        self.table.setEnabled(
            enabled
        )

        self.toolbar.setEnabled(
            enabled
        )

    # ---------------------------------------------------------

    def reload(self):

        self.refresh()