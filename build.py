from pathlib import Path
import shutil
import subprocess
import sys
import os


PROJECT = Path(__file__).parent.resolve()

DIST = PROJECT / "dist"
BUILD = PROJECT / "build"

EXE_NAME = "ExcelSvodka"


def remove(path: Path):
    if path.exists():
        shutil.rmtree(path)


def main():

    print("=" * 60)
    print("Сборка ExcelSvodka")
    print("=" * 60)

    remove(BUILD)

    spec = PROJECT / f"{EXE_NAME}.spec"

    if spec.exists():
        spec.unlink()

    separator = ";" if os.name == "nt" else ":"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",

        "--clean",
        "--noconfirm",
        "--windowed",

        "--name",
        EXE_NAME,

        "--add-data",
        f"data{separator}data",

        "run_gui.py",
    ]

    print("\nКоманда:")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\nСборка завершилась ошибкой.")
        sys.exit(result.returncode)

    exe = DIST / EXE_NAME / (
        f"{EXE_NAME}.exe"
        if os.name == "nt"
        else EXE_NAME
    )

    print("\n========================================")
    print("Сборка успешно завершена.")
    print("Файл находится:")
    print(exe)
    print("========================================")


if __name__ == "__main__":
    main()