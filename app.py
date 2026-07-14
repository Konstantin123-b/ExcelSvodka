from core.excel_manager import ExcelManager
from core.svodka_engine import SvodkaEngine


def ask_excel():
    while True:
        filename = input("\nПуть к Excel: ").strip()

        try:
            excel = ExcelManager()
            excel.open(filename)
            return excel

        except Exception as e:
            print(f"\nОшибка: {e}")


def menu():

    print("\n==============================")
    print(" ExcelSvodka")
    print("==============================")
    print("1. Добавить работу")
    print("2. Перенести простои")
    print("3. Сохранить")
    print("0. Выход")


def main():

    excel = ask_excel()

    engine = SvodkaEngine(excel)

    while True:

        menu()

        cmd = input("\nВыберите пункт: ").strip()

        if cmd == "0":
            break

        elif cmd == "1":

            garage = input("Гаражный номер: ").strip()

            model = input("Модель: ").strip()

            date = input("Дата: ").strip()

            code = input("Код: ").strip()

            work = input("Работа: ").strip()

            employees = input(
                "Исполнители (через запятую): "
            ).strip()

            employees = [
                x.strip()
                for x in employees.split(",")
                if x.strip()
            ]

            engine.add_work(
                garage_number=garage,
                model=model,
                date=date,
                code=code,
                work=work,
                employees=employees,
            )

            print("\nРабота добавлена.")

        elif cmd == "2":

            date = input(
                "Перенести простой с даты: "
            ).strip()

            result = engine.transfer_idle(date)

            print(
                f"\nПеренесено: {len(result)}"
            )

        elif cmd == "3":

            excel.save()

            print("\nКнига сохранена.")

        else:

            print("\nНеизвестная команда.")


if __name__ == "__main__":
    main()