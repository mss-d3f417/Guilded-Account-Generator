#Code By MSS.D3F417
#A super simple tool for creating multiple accounts on the Guilded platform
#Don't Copy & Paste KIDI (I SEE YOU)
#https://github.com/mss-d3f417

import sys
import requests
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class UserCreationThread(QThread):
    progress_updated = pyqtSignal(int)
    log_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_creation_url = "https://www.guilded.gg/api/users?type=email"
        self.user_creation_headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "guilded_mid=e9478a23-d836-4f94-9e6a-fc56d48d89e9; guilded_ipah=f977fb2bf60e64faea6d1ccb5c9a336f",
            "guilded-client-id": "e9478a23-d836-4f94-9e6a-fc56d48d89e9",
            "guilded-stag": "912e80c6496baa613f233151dd6782d4",
            "guilded-viewer-platform": "desktop",
            "Host": "www.guilded.gg",
            "Origin": "https://www.guilded.gg",
            "Pragma": "no-cache",
            "Referer": "https://www.guilded.gg/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.user_creation_payload = {
            "extraInfo": {"platform": "desktop"},
            "name": "GeneratedByD3417",
            "password": "mss@800900",
            "fullName": "Gen By D3417",
        }
        self.stopped = False

    def run(self):
        for i in range(200):
            if self.stopped:
                break

            Gen = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            emailgen = f"{Gen}@d3f417.com"
            self.user_creation_payload["email"] = emailgen

            user_creation_response = requests.post(
                self.user_creation_url,
                headers=self.user_creation_headers,
                json=self.user_creation_payload
            )

            status_code = user_creation_response.status_code
            response_content = user_creation_response.text

            with open('Generated.txt', "a+") as f:
                f.write(f'{emailgen}:mss@800900\n')

            self.log_updated.emit(
                f'[GENERATED] {emailgen}:mss@800900\n'
                #f'User Creation Status Code: {status_code}\n'
                #f'User Creation Response Content: {response_content}\n\n'
            )
            self.progress_updated.emit((i + 1) * 100 // 200)

    def stop(self):
        self.stopped = True

class UserCreationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Advanced Guilded Account Generrator | BY MSS.D3F417')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.start_button = QPushButton('Start User Creation', self)
        self.start_button.clicked.connect(self.start_user_creation)

        self.stop_button = QPushButton('Stop User Creation', self)
        self.stop_button.clicked.connect(self.stop_user_creation)
        self.stop_button.setEnabled(False)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel(self)
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)

    def start_user_creation(self):
        self.thread = UserCreationThread(self)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.log_updated.connect(self.update_log)
        self.thread.finished.connect(self.user_creation_finished)

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("User creation in progress...")
        self.text_edit.clear()

        self.thread.start()

    def stop_user_creation(self):
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.stop()
            self.status_label.setText("User creation stopped.")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_log(self, message):
        self.text_edit.append(message)

    def user_creation_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("User creation completed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserCreationApp()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())