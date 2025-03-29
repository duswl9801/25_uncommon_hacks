import sys
from PySide6 import QtWidgets, QtCore, QtGui

def load_custom_font(font_path):
    font_id = QtGui.QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("Failed to load custom font from:", font_path)
        return None
    font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        print("Loaded custom font:", font_families[0])
        return font_families[0]
    return None

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)
        self.setup_ui()
        self.setStyleSheet("""
            QDialog {
                background-color: #000;
            }
            QLabel {
                color: #0f0;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #222;
                color: #0f0;
                border: 2px solid #0f0;
                padding: 5px;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QPushButton {
                background-color: #222;
                color: #0f0;
                border: 2px solid #0f0;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

    def setup_ui(self):
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton("Login")

        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.username_label, self.username_edit)
        form_layout.addRow(self.password_label, self.password_edit)
        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        # 간단한 로그인 검증 (실제 환경에서는 보안에 유의)
        if username == "admin" and password == "1234":
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect username or password")

class TimerDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Timer")
        self.setFixedSize(250, 150)
        self.setup_ui()
        self.setStyleSheet("""
            QDialog {
                background-color: #000;
            }
            QLabel {
                color: #0f0;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QSpinBox {
                background-color: #222;
                color: #0f0;
                border: 2px solid #0f0;
                padding: 5px;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QPushButton {
                background-color: #222;
                color: #0f0;
                border: 2px solid #0f0;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

    def setup_ui(self):
        self.hours_label = QtWidgets.QLabel("Hours:")
        self.minutes_label = QtWidgets.QLabel("Minutes:")
        self.hours_spin = QtWidgets.QSpinBox()
        self.hours_spin.setRange(0, 23)
        self.minutes_spin = QtWidgets.QSpinBox()
        self.minutes_spin.setRange(0, 59)
        self.start_button = QtWidgets.QPushButton("Start Timer")

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.hours_label, self.hours_spin)
        form_layout.addRow(self.minutes_label, self.minutes_spin)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.accept)

    def get_total_seconds(self):
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        return hours * 3600 + minutes * 60

# 메인 창 (레트로 디자인 적용, 항상 위에 표시됨)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, custom_font_family=None):
        super().__init__()
        self.setWindowTitle("Retro Game Theme")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(layout)

        self.cheat_button = QtWidgets.QPushButton("HELP")
        self.timer_button = QtWidgets.QPushButton("TIMER")
        self.quit_button = QtWidgets.QPushButton("QUIT")

        layout.addWidget(self.cheat_button)
        layout.addWidget(self.timer_button)
        layout.addWidget(self.quit_button)

        self.quit_button.clicked.connect(QtWidgets.QApplication.quit)
        self.timer_button.clicked.connect(self.open_timer_dialog)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #000;
            }
            QPushButton {
                background-color: #222;
                color: #0f0;
                border: 2px solid #0f0;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

        if custom_font_family:
            font = QtGui.QFont(custom_font_family, 10)
        else:
            font = QtGui.QFont("Courier New", 10)
        self.setFont(font)

    def open_timer_dialog(self):
        dialog = TimerDialog()
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            total_seconds = dialog.get_total_seconds()
            if total_seconds == 0:
                QtWidgets.QMessageBox.information(self, "Timer", "타이머 시간이 0으로 설정되었습니다.")
                return
            # 타이머 시간(ms) 계산 및 타이머 시작
            QtCore.QTimer.singleShot(total_seconds * 1000, self.timer_finished)
            QtWidgets.QMessageBox.information(self, "Timer", f"타이머가 {total_seconds // 3600}시간 { (total_seconds % 3600) // 60}분 후에 울립니다.")

    def timer_finished(self):
        QtWidgets.QMessageBox.warning(self, "Timer", "설정한 시간이 지났습니다!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    font_path = "resource/font/PressStart2P-Regular.ttf"
    font_family = load_custom_font(font_path)

    login = LoginDialog()
    if font_family:
        login.setFont(QtGui.QFont(font_family, 12))
    if login.exec() == QtWidgets.QDialog.Accepted:
        window = MainWindow(custom_font_family=font_family)
        window.show()
        sys.exit(app.exec())
