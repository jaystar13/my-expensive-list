from repositories.db_expense_repository import BaseExpenseRepository


class GoogleSheetsExpenseRepository(BaseExpenseRepository):
    def __init__(self, sheet_id: str, credentials_path: str):
        self.sheet_id = sheet_id
        self.credentials_path = credentials_path

    def save_expenses(self, expenses):
        """지출 내역 Google 스프레드시트에 저장"""
        pass
