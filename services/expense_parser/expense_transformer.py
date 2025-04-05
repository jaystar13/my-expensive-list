from typing import Any, Dict, List
from entities.expense import Expense
from services.expense_parser.expense_parsers import (
    HanaCardParser,
    KBCardParser,
    KBankParser,
)


class ExpenseTransformer:
    """금융기관별 데이터를 Expense 객체로 변환하는 서비스"""

    PARSERS = {
        "hana-card": HanaCardParser(),
        "kb-card": KBCardParser(),
        "k-bank": KBankParser(),
    }

    @classmethod
    def transform(cls, raw_data: List[Dict[str, Any]]) -> List[Expense]:
        expenses = []
        for item in raw_data:
            financial_name = item["financial_name"]
            parser = cls.PARSERS.get(financial_name)

            if parser:
                expenses.extend(parser.parse(item["data"]))
            else:
                print(f"경고: {financial_name}에 대한 파서가 존재하지 않습니다.")

        return expenses
