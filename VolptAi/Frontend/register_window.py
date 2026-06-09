from PyQt6.QtWidgets import *

from api_client import ApiClient


class RegisterWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.api = ApiClient()

        self.setWindowTitle(
            "Регистрация"
        )

        self.resize(400, 300)

        layout = QVBoxLayout()

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Логин"
        )

        self.email = QLineEdit()

        self.email.setPlaceholderText(
            "Email"
        )

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Пароль"
        )

        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.register_btn = QPushButton(
            "Зарегистрироваться"
        )

        self.register_btn.clicked.connect(
            self.register
        )

        layout.addWidget(
            self.username
        )

        layout.addWidget(
            self.email
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            self.register_btn
        )

        self.setLayout(layout)

    def register(self):

        result = self.api.register(

            self.username.text(),

            self.email.text(),

            self.password.text()
        )

        if "id" in result:

            QMessageBox.information(

                self,

                "Успех",

                "Пользователь успешно зарегистрирован"
            )

            self.close()

        else:

            QMessageBox.warning(

                self,

                "Ошибка",

                str(result)
            )