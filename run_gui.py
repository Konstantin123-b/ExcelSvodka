import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from gui.main_window import MainWindow


def exception_hook(exc_type, exc_value, exc_traceback):
    """
    Глобальный обработчик необработанных исключений.
    """

    text = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback,
        )
    )

    print(text)

    QMessageBox.critical(
        None,
        "Критическая ошибка",
        text,
    )


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("ExcelSvodka")
    app.setOrganizationName("ExcelSvodka")

    sys.excepthook = exception_hook

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()