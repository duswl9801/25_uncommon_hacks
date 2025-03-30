import sys
from PySide6 import QtWidgets, QtCore, QtGui
from guide.guide import Guide
import asyncio

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

class LoginPage(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #0E1323;
            }
            QLabel {
                color: #4CF190;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 5px;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #4CF190;
                color: #0E1323;
            }
        """)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        self.username_label = QtWidgets.QLabel("Username:")
        self.username_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        form_layout.addRow(self.username_label, self.username_edit)
        form_layout.addRow(self.password_label, self.password_edit)
        layout.addLayout(form_layout)
        self.login_button = QtWidgets.QPushButton("Login")
        layout.addWidget(self.login_button)
        self.setLayout(layout)
        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        # TODO - Connect Login
        if username == "admin" and password == "1234":
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect username or password")

class MenuPage(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #0E1323;
            }
            QPushButton {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #4CF190;
                color: #0E1323;
            }
        """)

    def setup_ui(self):
        layout = QtWidgets.QHBoxLayout()
        self.cheat_button = QtWidgets.QPushButton("HELP")
        self.timer_button = QtWidgets.QPushButton("TIMER")
        self.quit_button = QtWidgets.QPushButton("QUIT")
        layout.addWidget(self.cheat_button)
        layout.addWidget(self.timer_button)
        layout.addWidget(self.quit_button)
        self.setLayout(layout)

        self.quit_button.clicked.connect(QtWidgets.QApplication.quit)
        self.timer_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.timer_page))
        self.cheat_button.clicked.connect(self.handle_cheat)

    def handle_cheat(self):
        # TODO - LLM
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.info_alert_page)

class TimerPage(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #0E1323;
            }
            QLabel {
                color: #4CF190;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QSpinBox {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 5px;
                font-family: "Press Start 2P", cursive;
                font-size: 12px;
            }
            QPushButton {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #4CF190;
                color: #0E1323;
            }
        """)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        self.hours_label = QtWidgets.QLabel("Hours:")
        self.hours_spin = QtWidgets.QSpinBox()
        self.hours_spin.setRange(0, 23)
        self.minutes_label = QtWidgets.QLabel("Minutes:")
        self.minutes_spin = QtWidgets.QSpinBox()
        self.minutes_spin.setRange(0, 59)
        form_layout.addRow(self.hours_label, self.hours_spin)
        form_layout.addRow(self.minutes_label, self.minutes_spin)
        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.set_button = QtWidgets.QPushButton("Set")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(self.set_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.set_button.clicked.connect(self.set_timer)
        self.cancel_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page))

    def set_timer(self):
        hours = self.hours_spin.value()
        minutes = self.minutes_spin.value()
        total_seconds = hours * 3600 + minutes * 60
        if total_seconds == 0:
            # 타이머 시간이 0이면 InfoAlertPage 표시
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.info_alert_page)
        else:
            self.main_window.user_timer = QtCore.QTimer(self)
            self.main_window.user_timer.setSingleShot(True)
            self.main_window.user_timer.timeout.connect(self.main_window.show_timer_alert_page)
            self.main_window.user_timer.start(total_seconds * 1000)
            self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page)

class TimerAlertPage(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #0E1323;
            }
            QLabel {
                color: #4CF190;
                font-family: "Press Start 2P", cursive;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #4CF190;
                color: #0E1323;
            }
        """)
        self.auto_close_timer = QtCore.QTimer(self)
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.auto_close)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.message_label = QtWidgets.QLabel("Time's up! Ready to take a break?")
        layout.addWidget(self.message_label)
        button_layout = QtWidgets.QHBoxLayout()
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.ignore_button = QtWidgets.QPushButton("Ignore")
        button_layout.addWidget(self.quit_button)
        button_layout.addWidget(self.ignore_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.quit_button.clicked.connect(QtWidgets.QApplication.quit)
        self.ignore_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page))

    def showEvent(self, event):
        super().showEvent(event)
        self.auto_close_timer.start(10000)

    def auto_close(self):
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page)

class InfoAlertPage(QtWidgets.QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #0E1323;
            }
            QLabel {
                color: #4CF190;
                font-family: "Press Start 2P", cursive;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0E1323;
                color: #4CF190;
                border: 2px solid #4CF190;
                padding: 10px;
                font-size: 16px;
                font-family: "Press Start 2P", cursive;
            }
            QPushButton:hover {
                background-color: #4CF190;
                color: #0E1323;
            }
        """)

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout()
        ################################################
        guide = Guide()
        best_description = guide.findMostSimilarImage()
        guide_message = guide.printGuide(best_description)
        ################################################
        self.message_label = QtWidgets.QLabel(guide_message)
        layout.addWidget(self.message_label)
        self.ok_button = QtWidgets.QPushButton("OK")
        layout.addWidget(self.ok_button)
        self.setLayout(layout)
        self.ok_button.clicked.connect(lambda: self.main_window.stacked_widget.setCurrentWidget(self.main_window.menu_page))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, custom_font_family=None):
        super().__init__()
        self.setWindowTitle("Game Catcher")
        # self.setGeometry(100, 100, 100, 150)
        self.resize(350, 150)
        self.setMinimumSize(350, 150)
        if custom_font_family:
            self.custom_font = QtGui.QFont(custom_font_family, 10)
        else:
            self.custom_font = QtGui.QFont("Courier New", 10)
        self.setFont(self.custom_font)
        self.user_timer = None

        # manage several windows by using QStackedWidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #0E1323;")
        self.setCentralWidget(self.stacked_widget)

        self.login_page = LoginPage(self)
        self.menu_page = MenuPage(self)
        self.timer_page = TimerPage(self)
        self.timer_alert_page = TimerAlertPage(self)
        self.info_alert_page = InfoAlertPage(self)

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.timer_page)
        self.stacked_widget.addWidget(self.timer_alert_page)
        self.stacked_widget.addWidget(self.info_alert_page)

        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_timer_alert_page(self):
        self.stacked_widget.setCurrentWidget(self.timer_alert_page)


def startGameCatcher():
    app = QtWidgets.QApplication(sys.argv)
    font_path = "assets/PressStart2P-Regular.ttf"
    font_family = load_custom_font(font_path)
    main_window = MainWindow(custom_font_family=font_family)
    main_window.show()
    sys.exit(app.exec())

"""
if __name__ == "__main__":
"""

