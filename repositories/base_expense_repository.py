from abc import ABC, abstractmethod
from typing import List

from entities.expense import Expense


class BaseExpenseRepository(ABC):
    @abstractmethod
    def save_expenses(self, expenses: List[Expense]):
        pass
