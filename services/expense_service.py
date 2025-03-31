import json
from dto.expense_search_dto import ExpenseSearchDto
from repositories.expese_repository import ExpenseRepository
from services.expense_reader.expense_reader_factory import ExpenseReaderFactory
from utils.os_utils import FileUtils

class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.expense_repository = repository

    def get_raw_expense_list(self, searchDto: ExpenseSearchDto):
        all_expenses = {}

        list_files = FileUtils.list_files(searchDto.directory_path, full_path=True)
        for file in list_files:
            try:
                reader = ExpenseReaderFactory.get_reader(file, searchDto.password)
                financial_name = reader.get_financial_name()
                financial_expenses = reader.fetch_expense_list()

                if financial_name not in all_expenses:
                    all_expenses[financial_name] = {"financial_name": financial_name, "data": []}
                
                all_expenses[financial_name]["data"].extend(financial_expenses)

            except ValueError as e:
                print(f"오류 발생: {e}")

        return json.dumps(list(all_expenses.values()), ensure_ascii=False, indent=4)