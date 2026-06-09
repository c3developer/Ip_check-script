from PyQt6.QtWidgets import *

from api_client import ApiClient
from main_window import MainWindow
from register_window import RegisterWindow

import session_store


class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.api = ApiClient()

        self.setWindowTitle(
            "VOLPT AI - Login"
        )

        self.resize(400, 250)

        layout = QVBoxLayout()

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Username"
        )

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Password"
        )

        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.login_button = QPushButton(
            "Login"
        )

        self.login_button.clicked.connect(
            self.login
        )

        self.register_button = QPushButton(
            "Регистрация"
        )

        self.register_button.clicked.connect(
            self.open_register
        )

        layout.addWidget(
            self.username
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            self.login_button
        )

        layout.addWidget(
            self.register_button
        )

        self.setLayout(layout)

    def login(self):

        result = self.api.login(

            self.username.text(),

            self.password.text()

        )
        

        if "access_token" in result:

            session_store.TOKEN = result["access_token"]

            session_store.USERNAME = self.username.text()

            self.main = MainWindow()

            self.main.show()

            self.close()

        else:

            QMessageBox.warning(

                self,

                "Ошибка",

                "Неверный логин или пароль"
            )

    def open_register(self):

        self.register_window = RegisterWindow()

        self.register_window.show()