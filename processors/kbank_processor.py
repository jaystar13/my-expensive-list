from processors.bank_processors import BankProcessor

import msoffcrypto
import io
import pandas as pd
from openpyxl import load_workbook

PASSWORD = "791227"

class KbankProcessor(BankProcessor):
    def process(self, file_path):
        print(f"케이뱅크 데이터 처리 중: {file_path}")
        try:
            decrypted = io.BytesIO()
            with open(file_path, "rb") as f:
                office_file = msoffcrypto.OfficeFile(f)
                office_file.load_key(password=PASSWORD)
                office_file.decrypt(decrypted)

            wb = load_workbook(filename=decrypted, read_only=True)
            sheet = wb.active

            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append(row)

            df = pd.DataFrame(data[1:], columns=data[0])
            print(f"DateFrame : {df.head()}")
        
        except Exception as e:
            print(f"파일을 읽는 중 오류 발생: {e}")
            return None