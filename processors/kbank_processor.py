from bank_processors import BankProcessor

class KbankProcessor(BankProcessor):
    def process(self, file_path):
        print(f"케이뱅크 데이터 처리 중: {file_path}")