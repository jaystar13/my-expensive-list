from typing import Any, Dict, List
from entities.expense import Expense
from services.expense_parser.base_parser import BaseParser

class HanaCardParser(BaseParser):
    def parse(self, data: List[Dict[str, Any]]) -> List[Expense]:
        expenses = []
        for entry in data:
            usage_date = self._convert_date(entry["date"])
            payment_year_month = usage_date[:7]
            expense = Expense(
                usage_date=usage_date,
                payment_year_month=payment_year_month,
                payment_method="하나카드",
                merchant_name=entry["merchant"],
                merchant_detail_name="",
                amount=int(entry["amount"].replace(",", "")),
            )
            expenses.append(expense)
        return expenses

    @staticmethod
    def _convert_date(date_str: str) -> str:
        """ 03/12 → 2025-03-12 형식으로 변환 (올해 기준) """
        return f"2025-{date_str[:2]}-{date_str[3:]}"


class KBCardParser(BaseParser):
    def parse(self, data: List[Dict[str, Any]]) -> List[Expense]:
        expenses = []
        for entry in data:
            usage_date = self._convert_date(entry["date"])
            payment_year_month = usage_date[:7]
            expense = Expense(
                usage_date=usage_date,
                payment_year_month=payment_year_month,
                payment_method=entry["cardName"],
                merchant_name=entry["merchant"],
                merchant_detail_name="",
                amount=int(entry["amount"].replace(",", "")),
            )
            expenses.append(expense)
        return expenses

    @staticmethod
    def _convert_date(date_str: str) -> str:
        """ 25.02.13 → 2025-02-13 """
        return "20" + date_str.replace(".", "-")


class KBankParser(BaseParser):
    def parse(self, data: List[Dict[str, Any]]) -> List[Expense]:
        expenses = []
        for entry in data:
            usage_date = entry["거래일시"].split(" ")[0].replace(".", "-")
            payment_year_month = usage_date[:7]
            expense = Expense(
                usage_date=usage_date,
                payment_year_month=payment_year_month,
                payment_method="K뱅크",
                merchant_name=entry["적요내용"],
                merchant_detail_name="",
                amount=entry["출금금액"],
            )
            expenses.append(expense)
        return expenses