from processors.bank_processors import BankProcessor
from processors.response import FinancialTransaction

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class HanaCardProcessor(BankProcessor):
    def process(self, file_path, password):
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

        return FinancialTransaction(financial="hana", transactions=transactions)

    def cleaner(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')

        transactions = []
        rows = soup.find_all("tr")  # 모든 행 찾기

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:  # 최소 3개의 열이 있어야 함
                usage_date = cells[0].get_text(strip=True)  # 이용일자
                merchant = cells[1].get_text(strip=True)  # 이용가맹점(은행)
                amount = cells[2].get_text(strip=True)  # 이용금액
                
                # 데이터 필터링 (날짜 형식 확인)
                # if "/" in usage_date and amount.replace(",", "").isdigit():
                #     transactions.append((usage_date, merchant, amount))

                if "/" in usage_date and amount.replace(",", "").isdigit():
                    transactions.append({
                        "date": "2025-" + usage_date.replace("/", "-"),
                        "cardName": "하나카드",
                        "merchant": merchant,
                        "amount": int(amount.replace(",", "").replace("₩", "")),
                    })                    

        # for t in transactions:
        #     print(f"이용일자: {t[0]}, 이용가맹점: {t[1]}, 이용금액: {t[2]}")

        return transactions        