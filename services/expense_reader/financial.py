from abc import ABC, abstractmethod
from typing import Dict, List


class Financial(ABC):
    @abstractmethod
    def get_financial_name(self) -> str:
        pass

    @abstractmethod
    def fetch_expense_list(self) -> List[Dict]:
        pass
