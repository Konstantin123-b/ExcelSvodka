from __future__ import annotations

import json
from pathlib import Path


class SettingsManager:
    """
    Работа с пользовательскими настройками.

    Настройки хранятся в data/settings.json
    """

    DEFAULTS = {
        "last_file": "",
        "window_width": 1400,
        "window_height": 900,
    }

    def __init__(self, filename: str = "data/settings.json"):

        self.path = Path(filename)

        self.data = {}

        self.load()

    # ---------------------------------------------------------

    def load(self) -> None:

        if not self.path.exists():

            self.data = dict(self.DEFAULTS)

            self.save()

            return

        try:

            with self.path.open(
                "r",
                encoding="utf-8",
            ) as file:

                self.data = json.load(file)

        except Exception:

            self.data = {}

        for key, value in self.DEFAULTS.items():

            self.data.setdefault(key, value)

    # ---------------------------------------------------------

    def save(self) -> None:

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    # ---------------------------------------------------------

    def get(self, key: str, default=None):

        return self.data.get(key, default)

    # ---------------------------------------------------------

    def set(self, key: str, value) -> None:

        self.data[key] = value

        self.save()

    # ---------------------------------------------------------

    @property
    def last_file(self) -> str:

        return self.get("last_file", "")

    @last_file.setter
    def last_file(self, value: str) -> None:

        self.set("last_file", value)

    # ---------------------------------------------------------

    @property
    def window_size(self) -> tuple[int, int]:

        return (
            int(self.get("window_width", 1400)),
            int(self.get("window_height", 900)),
        )

    @window_size.setter
    def window_size(self, size: tuple[int, int]) -> None:

        width, height = size

        self.data["window_width"] = int(width)
        self.data["window_height"] = int(height)

        self.save()