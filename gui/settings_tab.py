from pathlib import Path
import json

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SettingsTab(QWidget):
    """
    Вкладка настроек приложения.

    Не зависит от core.
    Работает только с data/settings.json.
    """

    settings_changed = Signal(dict)

    SETTINGS_FILE = Path("data/settings.json")

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        group = QGroupBox("Настройки")
        form = QFormLayout(group)

        self.default_excel = QLineEdit()

        browse = QPushButton("...")

        browse.clicked.connect(
            self.select_excel
        )

        excel_layout = QHBoxLayout()
        excel_layout.addWidget(self.default_excel)
        excel_layout.addWidget(browse)

        form.addRow(
            "Файл Excel",
            excel_layout,
        )

        self.author = QLineEdit()

        form.addRow(
            "Пользователь",
            self.author,
        )

        self.backup = QCheckBox(
            "Создавать резервную копию"
        )

        form.addRow(
            "",
            self.backup,
        )

        self.autosave = QCheckBox(
            "Автоматически сохранять"
        )

        form.addRow(
            "",
            self.autosave,
        )

        self.history = QSpinBox()
        self.history.setRange(10, 10000)
        self.history.setValue(200)

        form.addRow(
            "Размер журнала",
            self.history,
        )

        layout.addWidget(group)

        self.save_button = QPushButton(
            "Сохранить настройки"
        )

        layout.addWidget(
            self.save_button
        )

        layout.addStretch()

        self.status = QLabel("")

        layout.addWidget(
            self.status
        )

        self.save_button.clicked.connect(
            self.save_settings
        )

        self.load_settings()

    def select_excel(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите Excel",
            "",
            "Excel (*.xlsx *.xlsm)",
        )

        if filename:
            self.default_excel.setText(filename)

    def load_settings(self):

        if not self.SETTINGS_FILE.exists():
            return

        try:

            with open(
                self.SETTINGS_FILE,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

            self.default_excel.setText(
                data.get(
                    "default_excel",
                    "",
                )
            )

            self.author.setText(
                data.get(
                    "author",
                    "",
                )
            )

            self.backup.setChecked(
                data.get(
                    "backup",
                    True,
                )
            )

            self.autosave.setChecked(
                data.get(
                    "autosave",
                    True,
                )
            )

            self.history.setValue(
                data.get(
                    "history",
                    200,
                )
            )

        except Exception:

            self.status.setText(
                "Ошибка чтения settings.json"
            )

    def save_settings(self):

        self.SETTINGS_FILE.parent.mkdir(
            exist_ok=True
        )

        data = {
            "default_excel": self.default_excel.text().strip(),
            "author": self.author.text().strip(),
            "backup": self.backup.isChecked(),
            "autosave": self.autosave.isChecked(),
            "history": self.history.value(),
        }

        with open(
            self.SETTINGS_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4,
            )

        self.status.setText(
            "Настройки сохранены"
        )

        self.settings_changed.emit(data)