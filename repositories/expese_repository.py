import json
import os
from typing import List

from entities.expense import Expense


class ExpenseRepository:
    def __init__(self, storage_path: str):
        self.strage_path = storage_path

    def save_expenses(self, expenses: List[Expense]):
        """지출 내역을 JSON 파일로 저장"""
        file_path = os.path.join(self.strage_path, "expenses.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecoder:
                    existing_data = []
        else:
            existing_data = []

        # 새로운 데이터 추가
        new_data = [expense.to_dict() for expense in expenses]
        all_data = existing_data + new_data

        # 파일 저장
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(all_data, file, ensure_ascii=False, indent=4)