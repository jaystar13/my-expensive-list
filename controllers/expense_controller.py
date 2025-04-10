from dto.expense_search_dto import ExpenseSearchDto
from services.expense_service import ExpenseService


class ExpenseController:
    def __init__(self, service: ExpenseService):
        self.expense_service = service

    def clean(self, serarchDto: ExpenseSearchDto):
        # 지출 리스트 조회
        self.expense_service.save_expenses(serarchDto)
