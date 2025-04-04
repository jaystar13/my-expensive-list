import os
import sys
from PyQt5 import QtWidgets, uic

from dto.expense_search_dto import ExpenseSearchDto
from controllers.expense_controller import ExpenseController
from repositories.expese_repository import ExpenseRepository
from services.expense_parser.expense_transformer import ExpenseTransformer
from services.expense_service import ExpenseService

class AllMyExpenses(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/data-cleaner.ui", self)

        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        target_path = self.targetPath.text()
        target_date = self.targetYearMonth.date().toString('yyyy-MM')
        password = self.password.text()
        directory_path = os.path.join(target_path, target_date)
        raw_directory_path = os.path.join(directory_path, "raw")

        expense_repository = ExpenseRepository(directory_path, target_date + "_expenses.json")
        expense_transformer = ExpenseTransformer()
        expense_service = ExpenseService(expense_repository, expense_transformer)
        expense_controller = ExpenseController(expense_service)

        dto = ExpenseSearchDto(target_path, target_date, password, directory_path, raw_directory_path)
        expense_controller.clean(dto)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = AllMyExpenses()
    window.show()

    sys.exit(app.exec_())