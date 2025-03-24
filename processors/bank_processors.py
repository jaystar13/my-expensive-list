from abc import ABC, abstractmethod
from processors.response import FinancialTransaction

class BankProcessor(ABC):
    """은행 데이터 처리를 위한 추상 클래스"""

    @abstractmethod
    def process(self, file_path: str, password) -> FinancialTransaction:
        pass