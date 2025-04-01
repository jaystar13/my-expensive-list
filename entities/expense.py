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