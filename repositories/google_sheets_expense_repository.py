from typing import List
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from entities.expense import Expense
from repositories.db_expense_repository import BaseExpenseRepository


class GoogleSheetsExpenseRepository(BaseExpenseRepository):
    def __init__(self, sheet_id: str, credentials_path: str):
        self.sheet_id = sheet_id
        self.credentials_path = credentials_path

    def save_expenses(self, expenses: List[Expense]):
        """지출 내역 Google 스프레드시트에 저장"""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_path, scope
        )
        client = gspread.authorize(creds)
        sheet = client.open_by_key(self.sheet_id).sheet1

        headers = [
            "이용일",
            "결재월",
            "이용카드",
            "가맹정(상품)명",
            "상세상품명",
            "이용금액",
            "구분",
        ]
        sheet.clear()
        sheet.append_row(headers)

        for expense in expenses:
            row = [
                expense.usage_date,
                expense.payment_year_month,
                expense.payment_method,
                expense.merchant_name,
                expense.merchant_detail_name,
                expense.amount,
                expense.category,
            ]
            sheet.append_row(row)
