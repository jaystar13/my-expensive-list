import sys
from PyQt5 import QtWidgets, uic

from dto.expense_search_dto import ExpenseSearchDto
from controllers.expense_controller import ExpenseController

class AllMyExpenses(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/data-cleaner.ui", self)

        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        target_path = self.targetPath.text()
        target_date = self.targetYearMonth.date().toString('yyyy-MM')
        password = self.password.text()

        dto = ExpenseSearchDto(target_path, target_date, password)
        ExpenseController().clean(dto)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AllMyExpenses()
    window.show()
    sys.exit(app.exec_())