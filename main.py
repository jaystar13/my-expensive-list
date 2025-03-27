import os
import sys
from PyQt5 import QtWidgets, uic

from dto.expense_search_dto import ExpenseSearchDto
from controllers.expense_controller import ExpenseController
from repositories.expese_repository import ExpenseRepository
from services.expense_service import ExpenseService

class AllMyExpenses(QtWidgets.QMainWindow):
    def __init__(self, expense_controller):
        super().__init__()
        uic.loadUi("gui/data-cleaner.ui", self)
        self.expense_controller = expense_controller

        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        target_path = self.targetPath.text()
        target_date = self.targetYearMonth.date().toString('yyyy-MM')
        password = self.password.text()
        directory_path = os.path.join(target_path, target_date)
        dto = ExpenseSearchDto(target_path, target_date, password, directory_path)

        expense_controller.clean(dto)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    expense_repository = ExpenseRepository()
    expense_service = ExpenseService(expense_repository)
    expense_controller = ExpenseController(expense_service)

    window = AllMyExpenses(expense_controller)
    window.show()

    sys.exit(app.exec_())