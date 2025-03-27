from dataclasses import dataclass

@dataclass(frozen=True)
class ExpenseSearchDto:
    target_path: str
    target_date: str
    password: str