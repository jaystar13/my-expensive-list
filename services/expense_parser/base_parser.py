from abc import ABC, abstractmethod
from typing import Any, Dict, List

from entities.expense import Expense


class BaseParser(ABC):
    """금융기관별 데이터를 Expense 객체로 변환하는 기본 클래스"""

    @abstractmethod
    def parse(self, data: List[Dict[str, Any]]) -> List[Expense]:
        pass
