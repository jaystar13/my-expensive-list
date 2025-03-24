from processors.bank_processors import BankProcessor
from processors.response import FinancialTransaction

import msoffcrypto
import io
import pandas as pd
from openpyxl import load_workbook

class KbankProcessor(BankProcessor):
    def process(self, file_path, password):
        print(f"케이뱅크 데이터 처리 중: {file_path}")
        try:
            decrypted = io.BytesIO()
            with open(file_path, "rb") as f:
                office_file = msoffcrypto.OfficeFile(f)
                office_file.load_key(password=password)
                office_file.decrypt(decrypted)

            df = pd.read_excel(decrypted, engine="openpyxl", header=3)

            transactions = []
            for index, row in df.iterrows():
                # 체크결제 이용내역만 대상
                if row["거래구분"] == "체크결제":
                    usage_date = row["거래일시"] # 일자
                    card_name = "케이뱅크" # 카드명칭
                    merchant = row["적요내용"] # 가맹점
                    amount = row["출금금액"] # 이용금액
                    
                    transactions.append({
                        "date": usage_date.split()[0].replace(".", "-"),
                        "cardName": card_name,
                        "merchant": merchant,
                        "amount": amount,
                    })                    
        
        except Exception as e:
            print(f"파일을 읽는 중 오류 발생: {e}")
            return None
        
        return FinancialTransaction(financial="KBank", transactions=transactions)