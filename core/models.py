from dataclasses import dataclass
from enum import Enum


class MachineState(str, Enum):
    """
    Тип записи в суточной сводке.
    """

    IDLE = ">"
    ACCIDENT = "ав"
    PLANNED = "пл"
    CUSTOMER = "з"

    @property
    def title(self) -> str:
        return {
            MachineState.IDLE: "Простой",
            MachineState.ACCIDENT: "Аварийный ремонт",
            MachineState.PLANNED: "Плановые работы",
            MachineState.CUSTOMER: "Работы заказчика",
        }[self]

    @classmethod
    def from_code(cls, code: str):
        code = (code or "").strip().lower()

        for state in cls:
            if state.value == code:
                return state

        return None


@dataclass(slots=True)
class SvodkaRecord:
    """
    Одна запись сводки.
    """

    state: MachineState

    garage_number: str

    model: str

    description: str

    employees: str = ""
