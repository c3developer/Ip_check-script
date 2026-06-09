import sys

from PyQt6.QtWidgets import QApplication

from login_window import LoginWindow

app = QApplication(sys.argv)
app.setStyleSheet("""
QWidget {
    background-color: #1e1e1e;
    color: white;
    font-size: 12pt;
}

QTextEdit {
    background-color: #252526;
    border: 1px solid #404040;
}

QLineEdit {
    background-color: #252526;
    border: 1px solid #404040;
    padding: 6px;
}

QPushButton {
    background-color: #0e639c;
    border: none;
    padding: 8px;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #1177bb;
}

QListWidget {
    background-color: #252526;
}
""")

window = LoginWindow()

window.show()

sys.exit(
    app.exec()
)