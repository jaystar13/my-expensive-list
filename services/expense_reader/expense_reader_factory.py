from services.expense_reader.expense_readers import HanaCardExpenseReader, KBCardExpenseReader, KBankExpenseReader
from services.expense_reader.financial import Financial

class ExpenseReaderFactory:
    """ 파일명을 기반으로 적절한 ExpenseReader 클래스를 선택하는 팩토리 """

    @staticmethod
    def get_reader(file_path: str, password: str) -> Financial:
        if "케이뱅크" in file_path.lower() and file_path.endswith(".xlsx"):
            return KBankExpenseReader(file_path, password)
        elif "hanacard" in file_path.lower() and file_path.endswith(".html"):
            return HanaCardExpenseReader(file_path, password)
        elif "kb" in file_path.lower() and file_path.endswith(".html"):
            return KBCardExpenseReader(file_path, password)
        else:
            raise ValueError(f"지원하지 않는 파일 형식 또는 금융기관: {file_path}")
