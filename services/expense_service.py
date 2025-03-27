from dto.expense_search_dto import ExpenseSearchDto
from repositories.expese_repository import ExpenseRepository

class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.expense_repository = repository

    def clear(self, searchDto: ExpenseSearchDto):
        print(f"service's dto : {searchDto.target_date}")

    def get_raw_expense_list(self, searchDto: ExpenseSearchDto):
        pass