import sys
import os
import imaplib
import email
import re
from datetime import datetime
from email.header import decode_header
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDateTimeEdit

ATTACH_FOLDER = "downloads/attach"

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

def format_imap_date(date):
    """날짜를 IMAP 검색 형식 (DD-Mon-YYYY)으로 변환"""
    return date.strftime("%d-%b-%Y")        

def create_criteria(since_date):
    search_criteria = ["ALL"]
    if since_date:
        search_criteria += ["SINCE", format_imap_date(since_date)]

    return search_criteria

def save_attachment(emails, save_folder):
    """이메일에서 첨부 파일 저장"""

    os.makedirs(save_folder, exist_ok=True)

    for msg in emails:
        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", "")
            if part.get_content_maintype() == "multipart" or not content_disposition:
                continue  # 본문이거나 첨부파일이 없으면 스킵

            filename, encoding = decode_header(part.get_filename() or "")[0]
            if isinstance(filename, bytes):
                filename = filename.decode(encoding or "utf-8")

            if filename:
                filepath = os.path.join(save_folder, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))    

    # for part in msg.walk():
    #     content_disposition = part.get("Content-Disposition", "")
    #     if part.get_content_maintype() == "multipart" or not content_disposition:
    #         continue  # 본문이거나 첨부파일이 없으면 스킵

    #     filename, encoding = decode_header(part.get_filename() or "")[0]
    #     if isinstance(filename, bytes):
    #         filename = filename.decode(encoding or "utf-8")

    #     if filename:
    #         filepath = os.path.join(save_folder, filename)
    #         with open(filepath, "wb") as f:
    #             f.write(part.get_payload(decode=True))

    return [os.path.join(save_folder, filename) for filename in os.listdir(save_folder) if os.path.isfile(os.path.join(save_folder, filename))]    

class NaverMailClient:
    """네이버 메일에서 특정 정규식 패턴과 일치하는 메일을 검색하는 클래스"""

    def __init__(self, email_id, email_password):
        self.email_id = email_id
        self.email_password = email_password
        self.server = "imap.naver.com"

    def _decode_subject(self, subject):
        """이메일 제목 디코딩"""
        decoded, encoding = decode_header(subject)[0]
        return decoded.decode(encoding) if isinstance(decoded, bytes) else decoded
    
    def fetch_emails(self, search_criteria, patterns):
        """작성년월에 해당하는 메일을 검색하여 키워드 포함 메일 반환"""
        matching_mails = []
        keyword_regex = re.compile("|".join(patterns), re.IGNORECASE)
        try:
            with imaplib.IMAP4_SSL(self.server) as mail:
                mail.login(self.email_id, self.email_password)
                mail.select("INBOX")
                result, data = mail.search(None, *search_criteria)

                for num in data[0].split():
                    _, msg_data = mail.fetch(num, "(RFC822)")

                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 제목 디코딩
                    subject = self._decode_subject(msg["Subject"])

                    # 정규식으로 제목 필터링
                    if keyword_regex.search(subject):
                        # save_attachment(msg, ATTACH_FOLDER)  # 첨부 파일 저장
                        # matching_mails.append(subject)
                        matching_mails.append(msg)

        except imaplib.IMAP4.error as e:
            print(f"IMAP 오류 발생: {e}")
        except Exception as e:
            print(f"⚠️ 오류 발생: {e}")

        return matching_mails

class ExpenseApp(QtWidgets.QMainWindow):
    """GUI 앱 클래스"""

    # 체크박스 텍스트 → 정규식 매핑
    CHECKBOX_PATTERNS = {
        "KB": r"KB국민카드.*?명세서",
        "현대": r"현대카드.*?이용내역",
        "하나": r"하나카드.*?이용대금명세서",
        "네이버페이": r"네이버페이.*?사용내역",
        "케이뱅크": r"케이뱅크.*?거래내역"
    }    

    def __init__(self):
        super().__init__()
        uic.loadUi("spent-form.ui", self)  # UI 파일 로드

        # 실행 버튼 클릭 이벤트 연결
        self.extractSpentMail.clicked.connect(self.on_execute)

    def on_execute(self):
        naver_id = self.naverId.text()
        naver_password = self.naverPassword.text()
        targetDate = self.targetYearMonth.date().toString('yyyy-MM')
        selected_date = datetime.strptime(targetDate, "%Y-%m").date()

        mail_extract_status = self.maiExtractStatus
        mail_extract_status.setText("로그인 중...")
        QtWidgets.QApplication.processEvents()
        
        # 선택된 체크박스에 해당하는 정규식 패턴 추출
        selected_patterns = [
            self.CHECKBOX_PATTERNS[chkbox.text()]
            for chkbox in self.findChildren(QtWidgets.QCheckBox)
            if chkbox.isChecked() and chkbox.text() in self.CHECKBOX_PATTERNS
        ]

        mail_client = NaverMailClient(naver_id, naver_password)
        search_criteria = create_criteria(selected_date)

        mail_extract_status.setText("메일 검색 중...")
        QtWidgets.QApplication.processEvents()

        matching_emails = mail_client.fetch_emails(search_criteria, selected_patterns)

        targetAttachFolder = ATTACH_FOLDER + "/" + targetDate
        save_attachment(matching_emails, targetAttachFolder)

        mail_extract_status.setText("완료")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # UI 스타일 설정
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())