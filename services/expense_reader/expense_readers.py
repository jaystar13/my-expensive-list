import io
import msoffcrypto
import pandas as pd
from services.expense_reader.financial import Financial

class KBankExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        self.file_path = file_path
        self.password = password

    def fetch_expense_list(self):
        decrypted = io.BytesIO()
        with open(self.file_path, "rb") as f:
            office_file = msoffcrypto.OfficeFile(f)
            office_file.load_key(password=self.password)
            office_file.decrypt(decrypted)

        df = pd.read_excel(decrypted, engine="openpyxl", header=3)

        return df.to_dict(orient="records")
    
class HanaCardExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        super().__init__()

    def fetch_expense_list(self):
        print("HanaCardExpenseReader")
        return {}

class KBCardExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        super().__init__()

    def fetch_expense_list(self):
        print("KBCardExpenseReader")
        return {}