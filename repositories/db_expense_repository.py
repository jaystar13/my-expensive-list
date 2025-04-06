from repositories.base_expense_repository import BaseExpenseRepository


class DbExpenseRepository(BaseExpenseRepository):

    def __init__(self, db_url: str):
        self.db_url = db_url

    def save_expenses(self, expenses):
        pass
