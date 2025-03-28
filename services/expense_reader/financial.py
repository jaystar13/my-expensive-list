from abc import ABC, abstractmethod
from typing import Dict, List

class Financial(ABC):
    @abstractmethod
    def fetch_expense_list(self) -> List[Dict]:
        pass