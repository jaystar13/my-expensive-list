from bank_processors import BankProcessor

class KBProcessor(BankProcessor):
    def process(self, file_path):
        print(f"KB은행 데이터 처리 중: {file_path}")    