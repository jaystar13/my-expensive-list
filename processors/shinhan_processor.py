from processors.bank_processors import BankProcessor

class ShinhanProcessor(BankProcessor):
    def process(self, file_path, password):
        print(f"신한은행 데이터 처리 중: {file_path}")