import sys
import os
from PyQt5 import QtWidgets, uic
from processors.kb_processor import KBProcessor
from processors.hana_processor import HanaCardProcessor
from processors.kbank_processor import KbankProcessor
from processors.shinhan_processor import ShinhanProcessor

class DataCleaner(QtWidgets.QMainWindow):
    """GUI 앱 클래스"""

    def __init__(self):
        super().__init__()
        uic.loadUi("data-cleaner.ui", self)

        targetPath = self.targetPath.text()
        targetDate = self.targetYearMonth.date().toString('yyyy-MM')

        self.directory_path = os.path.join(targetPath, targetDate)

        # 은행명과 처리 클래스 매핑
        self.bank_processors = {
            "KB": KBProcessor(),
            "Shinhan": ShinhanProcessor(),
            "hanacard": HanaCardProcessor(),
            "케이뱅크": KbankProcessor()
        }

        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        """지정된 경로에서 파일을 순회하며 은행별 함수 실행"""
        if not os.path.isdir(self.directory_path):
            print(f"경로가 유효하지 않습니다: {self.directory_path}")
            return

        files = os.listdir(self.directory_path)
        if not files:
            print("디렉토리에 파일이 없습니다.")
            return

        for file_name in files:
            file_path = os.path.join(self.directory_path, file_name)
            if os.path.isfile(file_path):
                self.execute_bank_function(file_name, file_path)

    def execute_bank_function(self, file_name, file_path):
        """파일명을 기준으로 적절한 처리 클래스 실행"""
        for key, processor in self.bank_processors.items():
            if key in file_name:
                processor.process(file_path)
                return

        print(f"알 수 없는 파일 형식: {file_name}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DataCleaner()
    window.show()
    sys.exit(app.exec_())