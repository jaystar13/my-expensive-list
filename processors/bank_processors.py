from abc import ABC, abstractmethod

class BankProcessor(ABC):
    """은행 데이터 처리를 위한 추상 클래스"""

    @abstractmethod
    def process(self, file_path):
        pass