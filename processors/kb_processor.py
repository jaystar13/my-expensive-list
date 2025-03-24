from processors.bank_processors import BankProcessor
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from processors.response import FinancialTransaction

class KBProcessor(BankProcessor):
    def process(self, file_path, password):
        print(f"password : {password}")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # 브라우저 UI 없이 실행
        options.add_argument("--allow-file-access-from-files")
        driver = webdriver.Chrome(service=service, options=options)
        
        # html 파일 열기
        driver.get(f"file://{os.path.abspath(file_path)}")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)

        page_source = driver.page_source
        driver.quit()

        transactions = self.cleaner(page_source)

        return FinancialTransaction(financial="KB", transactions=transactions)

    def cleaner(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')

        table = soup.find("table", id="usage1")
        tbody = table.find("tbody", id="list_pe01")

        transactions = []
        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 6:
                continue # 필요한 데이터가 부족하면 건너뜀

            usage_date = cols[0].get_text(strip=True) # 이용일자
            card_name = cols[1].get_text(strip=True) # 이용카드
            merchant = cols[3].get_text(strip=True) # 가맹점
            amount = cols[5].get_text(strip=True) # 이용금액

            if card_name or card_name.strip() != "":
                transactions.append({
                    "date": "20" + usage_date.replace(".", "-"),
                    "cardName": card_name,
                    "merchant": merchant,
                    "amount": int(amount.replace(",", "").replace("₩", "")),
                })

        return transactions