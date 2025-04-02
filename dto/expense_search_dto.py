from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True)
class ExpenseSearchDto:
    target_path: str
    target_date: str
    password: str
    directory_path: str
    start_date: str = None
    end_date: str = None

    def __post_init__(self):
        year, month = map(int, self.target_date.split("-"))
        mid_date = datetime(year, month, 1) + timedelta(days=14)
        print(f"mid_date = {mid_date}")
        start_date = mid_date - timedelta(days=15)
        end_date = mid_date + timedelta(days=15)
        print(f"start_date = {start_date}, end_date = {end_date}")
        object.__setattr__(self, "start_date", start_date.strftime("%Y-%m-%d"))
        object.__setattr__(self, "end_date", end_date.strftime("%Y-%m-%d"))