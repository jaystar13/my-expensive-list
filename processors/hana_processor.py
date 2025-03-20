from bank_processors import BankProcessor

class HanaCardProcessor(BankProcessor):
    def process(self, file_path):
        print(f"하나카드 데이터 처리 중: {file_path}")