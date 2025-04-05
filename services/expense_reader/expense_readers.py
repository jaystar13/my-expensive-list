import io
import os
import time
from typing import Dict, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import msoffcrypto
import pandas as pd
from services.expense_reader.financial import Financial


class KBankExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        self.file_path = file_path
        self.password = password

    def get_financial_name(self) -> str:
        return "k-bank"

    def fetch_expense_list(self) -> List[Dict]:
        decrypted = io.BytesIO()
        with open(self.file_path, "rb") as f:
            office_file = msoffcrypto.OfficeFile(f)
            office_file.load_key(password=self.password)
            office_file.decrypt(decrypted)

        df = pd.read_excel(decrypted, engine="openpyxl", header=3)
        records = df.to_dict(orient="records")
        filtered_records = [
            record
            for record in records
            if self._is_expense(
                record.get("거래구분", ""),
                int(
                    str(record.get("출금금액", "0"))
                    .replace(",", "")
                    .replace("원", "")
                    .strip()
                    or 0
                ),
            )
        ]

        return filtered_records

    def _is_expense(self, type: str, amount: int) -> bool:
        if not type in ["체크결제", "전자금융"] or amount < 1000:
            return False
        return True


class HanaCardExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        self.file_path = os.path.abspath(file_path)
        self.password = password

        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 UI 없이 실행
        options.add_argument("--allow-file-access-from-files")
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_financial_name(self) -> str:
        return "hana-card"

    def open_and_decrypt_html(self) -> str:
        """Selenium을 이용해 보안 HTML 파일을 열고 패스워드를 입력한 후 페이지 HTML을 반환"""
        try:
            # HTML 파일 열기
            self.driver.get(f"file://{self.file_path}")

            # 패스워드 입력 필드 찾기 (id나 name 값은 직접 확인해서 변경해야 함)
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(self.password)  # 패스워드 입력
            password_input.send_keys(Keys.RETURN)  # 엔터 키 입력

            # 페이지가 로드될 때까지 잠시 대기
            time.sleep(3)  # 필요에 따라 조절 (명시적 대기를 쓰는 게 더 좋음)

            # 현재 페이지 HTML 가져오기
            page_source = self.driver.page_source
            return page_source

        except Exception as e:
            print(f"HTML 파일 복호화 중 오류 발생: {e}")
            return ""

        finally:
            self.driver.quit()  # 브라우저 닫기

    def fetch_expense_list(self) -> List[Dict]:
        print("HanaCardExpenseReader")
        html_content = self.open_and_decrypt_html()
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")

        rows = soup.find_all("tr")  # 모든 행 찾기

        transactions = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue  # 필요한 데이터가 부족하면 건너뜀

            usage_date = cols[0].get_text(strip=True)  # 이용일자
            merchant = cols[1].get_text(strip=True)  # 이용가맹점(은행)
            amount = cols[2].get_text(strip=True)  # 이용금액

            if "/" in usage_date and amount.replace(",", "").isdigit():
                transactions.append(
                    {
                        "date": cols[0].get_text(strip=True),
                        "cardName": "하나카드",
                        "merchant": merchant,
                        "amount": amount,
                    }
                )

        return transactions


class KBCardExpenseReader(Financial):
    def __init__(self, file_path: str, password: str):
        self.file_path = os.path.abspath(file_path)
        self.password = password

        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 UI 없이 실행
        options.add_argument("--allow-file-access-from-files")
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_financial_name(self) -> str:
        return "kb-card"

    def open_and_decrypt_html(self) -> str:
        """Selenium을 이용해 보안 HTML 파일을 열고 패스워드를 입력한 후 페이지 HTML을 반환"""
        try:
            # HTML 파일 열기
            self.driver.get(f"file://{self.file_path}")

            # 패스워드 입력 필드 찾기 (id나 name 값은 직접 확인해서 변경해야 함)
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(self.password)  # 패스워드 입력
            password_input.send_keys(Keys.RETURN)  # 엔터 키 입력

            # 페이지가 로드될 때까지 잠시 대기
            time.sleep(3)  # 필요에 따라 조절 (명시적 대기를 쓰는 게 더 좋음)

            # 현재 페이지 HTML 가져오기
            page_source = self.driver.page_source
            return page_source

        except Exception as e:
            print(f"HTML 파일 복호화 중 오류 발생: {e}")
            return ""

        finally:
            self.driver.quit()  # 브라우저 닫기

    def fetch_expense_list(self) -> List[Dict]:
        """복호화 후 HTML을 파싱하여 지출 데이터를 추출"""
        print("KBCardExpenseReader")
        html_content = self.open_and_decrypt_html()
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")

        table = soup.find("table", id="usage1")
        tbody = table.find("tbody", id="list_pe01")

        transactions = []

        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 6:
                continue  # 필요한 데이터가 부족하면 건너뜀

            card_name = cols[1].get_text(strip=True)  # 이용카드

            if card_name or card_name.strip() != "":
                transactions.append(
                    {
                        "date": cols[0].get_text(strip=True),
                        "cardName": card_name,
                        "merchant": cols[3].get_text(strip=True),
                        "amount": cols[5].get_text(strip=True),
                    }
                )

        return transactions
