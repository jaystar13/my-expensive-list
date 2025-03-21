from processors.bank_processors import BankProcessor
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

PASSWORD = "791227"

class KBProcessor(BankProcessor):
    def process(self, file_path):
        print(f"KB은행 데이터 처리 중: {file_path}")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # 브라우저 UI 없이 실행
        driver = webdriver.Chrome(options=options)
        
        # html 파일 열기
        driver.get(f"file://{os.path.abspath(file_path)}")

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)

        page_source = driver.page_source
        driver.quit()

        print(page_source)