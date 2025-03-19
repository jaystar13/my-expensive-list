import sys
import os
from PyQt5 import QtWidgets, uic

class DataCleaner(QtWidgets.QMainWindow):
    """GUI 앱 클래스"""

    def __init__(self):
        super().__init__()
        uic.loadUi("data-cleaner.ui", self)  # UI 파일 로드

        targetPath = self.targetPath.text()
        targetDate = self.targetYearMonth.date().toString('yyyy-MM')

        # 파일 경로 가져오기
        self.directory_path = targetPath + "/" + targetDate

        # 실행 버튼 클릭 이벤트 연결
        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        """지정된 경로에서 파일을 순회하며 출력"""
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
                print(f"파일 발견: {file_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # UI 스타일 설정
    window = DataCleaner()
    window.show()
    sys.exit(app.exec_())