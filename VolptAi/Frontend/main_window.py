from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from api_client import ApiClient
from settings_window import SettingsWindow
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import *
import session_store

class MainWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__()

        self.main_window = parent

        self.api = ApiClient()

        self.current_session = None

        self.setWindowTitle(
            "VOLPT AI"
        )

        self.resize(
            1200,
            700
        )

        self.build_ui()

        self.load_chats()

        self.apply_settings()
        

    def build_ui(self):

        root = QHBoxLayout()

        # Левая панель

        left = QVBoxLayout()

        self.new_chat_btn = QPushButton(
            "Новый чат"
        )

        self.new_chat_btn.clicked.connect(
            self.create_chat
        )

        self.settings_btn = QPushButton(
            "⚙ Настройки"
        )
        self.user_label = QLabel(
            f"👤 {session_store.USERNAME}"
        )

        self.user_label.setStyleSheet("""
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
    color: white;
    """)

        self.logout_btn = QPushButton(
            "🚪 Выйти"
        )   
        self.logout_btn.clicked.connect(
            self.logout
        )

        self.settings_btn.clicked.connect(
            self.open_settings
        )

        self.chat_list = QListWidget()
        self.chat_list.setContextMenuPolicy(
        Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.chat_list.customContextMenuRequested.connect(
        self.chat_menu
        )



        self.chat_list.itemClicked.connect(
            self.open_chat
        )

        left.addWidget(
            self.new_chat_btn
        )

        left.addWidget(
            self.settings_btn
        )
        left.addWidget(
            self.logout_btn
        )

        left.addWidget(
            self.chat_list
        )
        left.addWidget(
            self.user_label
        )
        # Правая панель

        right = QVBoxLayout()

        self.messages = QTextEdit()

        self.messages.setReadOnly(
            True
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Введите сообщение..."
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        self.send_btn = QPushButton(
            "Отправить"
        )

        self.send_btn.clicked.connect(
            self.send_message
        )

        right.addWidget(
            self.messages
        )

        right.addWidget(
            self.input
        )

        right.addWidget(
            self.send_btn
        )

        root.addLayout(
            left,
            1
        )

        root.addLayout(
            right,
            3
        )

        self.setLayout(
            root
        )


    def apply_settings(self):

        try:

            settings = self.api.get_settings()

            font = self.font()

            font.setPointSize(
                settings.get(
                    "font_size",
                    12
                )
            )

            self.setFont(font)

            if settings.get("theme") == "dark":

                self.setStyleSheet("""

                QWidget {
                    background-color: #212121;
                    color: white;
                    font-family: Segoe UI;
                }

                QListWidget {
                    background-color: #171717;
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                }

                QListWidget::item {
                    padding: 10px;
                    border-radius: 8px;
                }

                QListWidget::item:selected {
                    background-color: #343541;
                }

                QTextEdit {
                    background-color: #212121;
                    border: none;
                    padding: 10px;
                    color: white;
                }

                QLineEdit {
                    background-color: #2f2f2f;
                    border: 1px solid #444;
                    border-radius: 12px;
                    padding: 10px;
                    color: white;
                }

                QPushButton {
                    background-color: #2f2f2f;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    color: white;
                }

                QPushButton:hover {
                    background-color: #40414f;
                }

                """)

            else:

                self.setStyleSheet("""

                QListWidget {
                    background-color: white;
                    color: black;
                    border: 1px solid #cccccc;
                }

                QTextEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #cccccc;
                }

                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 1px solid #cccccc;
                }

                QPushButton {
                    background-color: #e5e5e5;
                    color: black;
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    padding: 8px;
                }

                """)

        except Exception as ex:

            print(
                "SETTINGS ERROR:",
                ex
            )
            
    def scroll_to_bottom(self):

        scrollbar = self.messages.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def load_chats(self):

        self.chat_list.clear()

        chats = self.api.get_chats()

        if isinstance(
                chats,
                dict
        ):

            QMessageBox.warning(

                self,

                "Ошибка",

                chats.get(
                    "detail",
                    "Ошибка загрузки"
                )
            )

            return

        for chat in chats:

            item = QListWidgetItem(
                chat["title"]
            )

            item.setData(

                Qt.ItemDataRole.UserRole,

                chat["id"]
            )

            self.chat_list.addItem(
                item
            )

    def create_chat(self):

        result = self.api.create_chat(
            "Новый чат"
        )

        self.load_chats()

        self.current_session = result["session_id"]

        for i in range(
                self.chat_list.count()
        ):

            item = self.chat_list.item(i)

            if item.data(
                    Qt.ItemDataRole.UserRole
            ) == self.current_session:

                self.chat_list.setCurrentItem(
                    item
                )

                self.messages.clear()

                break

    def open_chat(self, item):

        self.current_session = item.data(

            Qt.ItemDataRole.UserRole
        )

        self.messages.clear()

        history = self.api.get_history(
            self.current_session
        )

        if isinstance(
                history,
                dict
        ):

            QMessageBox.warning(

                self,

                "Ошибка",

                history.get(
                    "detail",
                    "Нет доступа"
                )
            )

            return

        for msg in history:

            if msg["role"] == "user":

                self.messages.append(
                    f"🧑 Вы:\n{msg['content']}\n"
                )

            else:

                self.messages.append(
                    f"🤖 VOLPT AI:\n{msg['content']}\n"
                )
        self.scroll_to_bottom()

    def send_message(self):

        if not self.current_session:

            QMessageBox.warning(
                self,
                "Внимание",
                "Выберите чат"
            )

            return

        text = self.input.text().strip()

        if not text:

            return

        self.messages.append(
            f"🧑 Вы:\n{text}\n"
        )

        self.scroll_to_bottom()

        self.input.clear()

        self.messages.append(
            "[assistant] Нейросеть думает..."
        )

        QApplication.processEvents()

        result = self.api.send_message(

            self.current_session,

            text
        )

        # ---------- АВТОПЕРЕИМЕНОВАНИЕ ----------

        current_item = None

        for i in range(
                self.chat_list.count()
        ):

            item = self.chat_list.item(i)

            if item.data(
                    Qt.ItemDataRole.UserRole
            ) == self.current_session:

                current_item = item
                break

        if current_item:

            if current_item.text() == "Новый чат":

                title = text[:30]

                self.api.rename_chat(
                    self.current_session,
                    title
                )

                current_item.setText(
                    title
                )

        # ----------------------------------------

        cursor = self.messages.textCursor()

        cursor.movePosition(
            cursor.MoveOperation.End
        )

        QApplication.processEvents()

        result = self.api.send_message(

            self.current_session,

            text
        )

        cursor = self.messages.textCursor()

        cursor.movePosition(

            cursor.MoveOperation.End
        )

        cursor.select(

            cursor.SelectionType.BlockUnderCursor
        )

        cursor.removeSelectedText()

        cursor.deletePreviousChar()

        if (

            isinstance(result, dict)

            and "response" in result

        ):

            self.messages.append(
                f"🤖 VOLPT AI:\n{result['response']}\n"
            )

        else:

            self.messages.append(

                f"🤖 VOLPT AI: Ошибка получения ответа"
            )

        self.scroll_to_bottom()

    def chat_menu(self, position):

        item = self.chat_list.itemAt(position)

        if not item:
            return

        menu = QMenu()

        rename_action = menu.addAction(
            "Переименовать"
        )

        delete_action = menu.addAction(
            "Удалить"
        )

        action = menu.exec(
            self.chat_list.mapToGlobal(position)
        )

        session_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if action == rename_action:

            title, ok = QInputDialog.getText(
                self,
                "Переименование",
                "Новое название:"
            )

            if ok and title:

                self.api.rename_chat(
                    session_id,
                    title
                )

                self.load_chats()

        elif action == delete_action:

            result = QMessageBox.question(
                self,
                "Удаление",
                "Удалить чат?"
            )

            if result == QMessageBox.StandardButton.Yes:

                self.api.delete_chat(
                    session_id
                )

                self.load_chats()

                self.messages.clear()

                self.current_session = None
    def open_settings(self):

        self.settings_window = SettingsWindow(self)

        self.settings_window.show()
    def logout(self):

        session_store.TOKEN = None

        from login_window import LoginWindow

        self.login_window = LoginWindow()

        self.login_window.show()

        self.close()