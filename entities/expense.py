class Expense:

    def __init__(self, usage_date: str, payment_year_month: str, payment_method: str,
                 merchant_name: str, merchant_detail_name: str, amount: int, category: str = "기타"):
        self.usage_date = usage_date
        self.payment_year_month = payment_year_month
        self.payment_method = payment_method
        self.merchant_name = merchant_name
        self.merchant_detail_name = merchant_detail_name
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f"Expense({self.usage_date}, {self.payment_year_month}, {self.payment_method}, {self.merchant_name}, {self.amount})"
    
    def to_dict(self):
        """Expense 객체를 JSON 저장을 위한 딕셔너리로 변환"""
        return {
            "usage_date": self.usage_date,
            "payment_year_month": self.payment_year_month,
            "payment_method": self.payment_method,
            "merchant_name": self.merchant_name,
            "merchant_detail_name": self.merchant_detail_name,
            "amount": self.amount,
            "category": self.category,
        }    