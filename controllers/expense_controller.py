from dto.expense_search_dto import ExpenseSearchDto

class ExpenseController:
    def __init__(self):
        pass

    def clean(self, dto: ExpenseSearchDto):
        print(f"target_path : {dto.target_path}")