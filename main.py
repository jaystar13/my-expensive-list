import os
import sys
from PyQt5 import QtWidgets, uic
from dotenv import load_dotenv

from config.repository_config import RepositoryConfig
from dto.expense_search_dto import ExpenseSearchDto
from controllers.expense_controller import ExpenseController
from repositories.expense_repository import ExpenseRepository
from repositories.expense_repository_factory import ExpenseRepositoryFactory
from services.expense_parser.expense_transformer import ExpenseTransformer
from services.expense_service import ExpenseService

load_dotenv()


class AllMyExpenses(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/data-cleaner.ui", self)

        self.cleanData.clicked.connect(self.on_execute)

    def on_execute(self):
        target_path = self.targetPath.text()
        target_date = self.targetYearMonth.date().toString("yyyy-MM")
        password = self.password.text()

        directory_path = os.path.join(target_path, target_date)
        raw_directory_path = os.path.join(directory_path, "raw")
        file_name = target_date + "_expenses.json"

        config = RepositoryConfig(
            storage_type=os.getenv("STORAGE_TYPE", "json"),
            directory_path=directory_path,
            file_name=file_name,
            sheet_id=os.getenv("GOOGLE_SHEET_ID"),
            credentials_path=os.getenv("GOOGLE_CREDENTIALS_PATH"),
        )

        repository = ExpenseRepositoryFactory.create(config)
        transformer = ExpenseTransformer()
        service = ExpenseService(repository, transformer)
        controller = ExpenseController(service)

        dto = ExpenseSearchDto(
            target_path, target_date, password, directory_path, raw_directory_path
        )
        controller.clean(dto)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = AllMyExpenses()
    window.show()

    sys.exit(app.exec_())
