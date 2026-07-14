from dataclasses import dataclass, field


@dataclass(slots=True)
class Equipment:
    row: int
    model: str
    garage_number: str


@dataclass(slots=True)
class JournalRecord:
    date: str
    model: str
    garage_number: str
    code: str
    description: str

    employees: list[str] = field(default_factory=list)

    customer_work: bool = False

    enabled: bool = True

@dataclass(slots=True)
class Equipment:
    row: int
    model: str
    garage_number: str


@dataclass(slots=True)
class Change:

    garage_number: str

    model: str

    date: str

    code: str

    work: str

    employees: list[str] = field(default_factory=list)