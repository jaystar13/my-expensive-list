from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    date: str
    cardName: str
    merchant: str
    amount: int

class FinancialTransaction(BaseModel):
    financial: str
    transactions: List[Transaction]