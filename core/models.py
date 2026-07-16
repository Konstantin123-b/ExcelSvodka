from dataclasses import dataclass
from enum import Enum


class MachineState(str, Enum):
    """
    Состояние машины в ежедневной сводке.
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
    def from_code(
        cls,
        code: str,
    ):

        code = (code or "").strip().lower()

        for state in cls:

            if state.value == code:
                return state

        return None

        
@dataclass(slots=True)
class Equipment:
    """
    Описание единицы техники.
    """

    row: int

    model: str

    garage_number: str


@dataclass(slots=True)
class SvodkaRecord:
    """
    Одна запись ежедневной сводки.
    """

    state: MachineState

    garage_number: str

    model: str

    description: str = ""

    operating_hours: str = ""

    employees: str = ""

    @property
    def code(self) -> str:
        return self.state.value

    @property
    def state_name(self) -> str:
        return self.state.title

    @property
    def code(self) -> str:
        if not isinstance(self.state, MachineState):
            raise TypeError(
                f"state={self.state!r}, type={type(self.state)}"
            )
        return self.state.value

    @property
    def code(self) -> str:
        if not isinstance(self.state, MachineState):
            import traceback

            raise TypeError(
                f"state={self.state!r}, "
                f"type={type(self.state)}\n\n"
                + "".join(traceback.format_stack())
            )

        return self.state.value
