from processors.bank_processors import BankProcessor
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

PASSWORD = "791227"

class KBProcessor(BankProcessor):
    def process(self, file_path):
        print(f"KB은행 데이터 처리 중: {file_path}")
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # 브라우저 UI 없이 실행
        options.add_argument("--allow-file-access-from-files")
        driver = webdriver.Chrome(service=service, options=options)
        
        # html 파일 열기
        driver.get(f"file://{os.path.abspath(file_path)}")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)

        page_source = driver.page_source
        driver.quit()

        self.cleaner(page_source)

    def cleaner(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')

        table = soup.find("table", id="usage1")
        tbody = table.find("tbody", id="list_pe01")

        data = []
        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 6:
                continue # 필요한 데이터가 부족하면 건너뜀

            usage_date = cols[0].get_text(strip=True) # 이용일자
            card_name = cols[1].get_text(strip=True) # 이용카드
            merchant = cols[3].get_text(strip=True) # 가맹점
            amount = cols[5].get_text(strip=True) # 이용금액

            if card_name or card_name.strip() != "":
                data.append({
                    "이용일자": usage_date,
                    "이용카드": card_name,
                    "가맹점": merchant,
                    "이용금액": amount,
                })

        return data