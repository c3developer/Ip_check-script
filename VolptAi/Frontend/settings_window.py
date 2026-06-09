from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from api_client import ApiClient


class SettingsWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__()

        self.setWindowFlag(
            Qt.WindowType.Window,
            True
        )

        self.api = ApiClient()

        self.setWindowTitle(
            "Настройки"
        )

        self.resize(500, 400)
        self.setMinimumSize(
            500,
            400
        )

        layout = QVBoxLayout()

        self.theme = QComboBox()

        self.theme.addItems(
            ["dark", "light"]
        )

        self.font_size = QSpinBox()

        self.font_size.setRange(
            10,
            16
        )

        self.model = QComboBox()

        self.model.addItems([
            "phi3:mini",
            "llama3.1:8b (скоро)",
            "qwen3:8b (скоро)"
        ])

        self.system_prompt = QTextEdit()
        self.system_prompt.setMaximumHeight(120)

        self.save_btn = QPushButton(
            "Сохранить"
        )

        self.save_btn.clicked.connect(
            self.save
        )

        layout.addWidget(
            QLabel("Тема")
        )

        layout.addWidget(
            self.theme
        )

        layout.addWidget(
            QLabel("Размер шрифта")
        )

        layout.addWidget(
            self.font_size
        )

        layout.addWidget(
            QLabel("Модель")
        )

        layout.addWidget(
            self.model
        )

        layout.addWidget(
            QLabel("Системный промпт")
        )

        layout.addWidget(
            self.system_prompt
        )

        layout.addWidget(
            self.save_btn
        )

        self.setLayout(layout)

        self.load_settings()
        

    def load_settings(self):

        data = self.api.get_settings()

        self.theme.setCurrentText(
            data["theme"]
        )

        self.font_size.setValue(
            data["font_size"]
        )

        self.model.setCurrentText(
            data["ai_model"]
        )

        self.system_prompt.setPlainText(
            data["system_prompt"]
        )

    def save(self):

        self.api.save_settings({
            "theme": self.theme.currentText(),
            "font_size": self.font_size.value(),
            "ai_model": self.model.currentText(),
            "system_prompt": self.system_prompt.toPlainText()
        })

        self.close()