from dataclasses import dataclass
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@dataclass(frozen=True)
class ExpenseSearchDto:
    target_path: str
    target_date: str
    password: str
    directory_path: str
    raw_directory_path: str
    start_date: str = None
    end_date: str = None

    def __post_init__(self):
        year, current_month = map(int, self.target_date.split("-"))
        current_date = datetime(year, current_month, 1)
        before_date = current_date - relativedelta(months=1)
        start_date = before_date + timedelta(days=14)
        end_date = current_date + timedelta(days=13)
        print(f"start_date = {start_date}, end_date = {end_date}")
        object.__setattr__(self, "start_date", start_date.strftime("%Y-%m-%d"))
        object.__setattr__(self, "end_date", end_date.strftime("%Y-%m-%d"))
