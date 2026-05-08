
import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QScrollArea,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from api_client import send_message_to_backend


class ChatWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        reply = send_message_to_backend(self.message)
        self.finished.emit(reply)


class MessageBubble(QFrame):
    def __init__(self, message, is_user=False, timestamp=""):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        outer_layout = QHBoxLayout()
        outer_layout.setContentsMargins(10, 4, 10, 4)

        bubble_container = QVBoxLayout()
        bubble_container.setSpacing(3)

        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.message_label.setMaximumWidth(380)
        self.message_label.setFont(QFont("Segoe UI", 10))

        self.time_label = QLabel(timestamp)
        self.time_label.setFont(QFont("Segoe UI", 8))
        self.time_label.setStyleSheet("color: #aaaaaa;")

        if is_user:
            self.message_label.setStyleSheet("""
                QLabel {
                    background-color: #0078d7;
                    color: white;
                    padding: 12px;
                    border-radius: 14px;
                }
            """)
            self.time_label.setAlignment(Qt.AlignRight)

            bubble_container.addWidget(self.message_label)
            bubble_container.addWidget(self.time_label)

            outer_layout.addStretch()
            outer_layout.addLayout(bubble_container)
        else:
            self.message_label.setStyleSheet("""
                QLabel {
                    background-color: #2a2a2a;
                    color: white;
                    padding: 12px;
                    border-radius: 14px;
                }
            """)
            self.time_label.setAlignment(Qt.AlignLeft)

            bubble_container.addWidget(self.message_label)
            bubble_container.addWidget(self.time_label)

            outer_layout.addLayout(bubble_container)
            outer_layout.addStretch()

        self.setLayout(outer_layout)


class ChatbotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOVA Assistant")
        self.setGeometry(250, 80, 720, 820)
        self.worker = None
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-family: Segoe UI;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color: white;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1b1b1b;
                border-radius: 14px;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(16, 14, 16, 14)

        title = QLabel("NOVA Assistant")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #aaaaaa; font-size: 11px;")

        header_layout.addWidget(title)
        header_layout.addWidget(self.status_label)
        header.setLayout(header_layout)

        # Scroll chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setContentsMargins(6, 6, 6, 6)
        self.chat_layout.setSpacing(6)
        self.chat_layout.addStretch()

        self.chat_container.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_container)

        # Input section
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #1b1b1b;
                border-radius: 14px;
            }
        """)
        input_layout_main = QVBoxLayout()
        input_layout_main.setContentsMargins(12, 12, 12, 12)
        input_layout_main.setSpacing(10)

        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
            }
            QPushButton:hover {
                background-color: #0062ad;
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        input_row.addWidget(self.message_input)
        input_row.addWidget(self.send_button)

        input_layout_main.addLayout(input_row)
        input_frame.setLayout(input_layout_main)

        main_layout.addWidget(header)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(input_frame)

        self.setLayout(main_layout)

    def current_time(self):
        return datetime.now().strftime("%I:%M %p")

    def add_message(self, message, is_user=False):
        timestamp = self.current_time()
        bubble = MessageBubble(message, is_user=is_user, timestamp=timestamp)

        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        QApplication.processEvents()
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):
        user_message = self.message_input.text().strip()

        if not user_message:
            return

        self.add_message(user_message, is_user=True)
        self.message_input.clear()

        self.status_label.setText("Thinking...")
        self.send_button.setEnabled(False)
        self.message_input.setEnabled(False)

        self.worker = ChatWorker(user_message)
        self.worker.finished.connect(self.handle_bot_reply)
        self.worker.start()

    def handle_bot_reply(self, reply):
        self.add_message(reply, is_user=False)

        self.status_label.setText("Ready")
        self.send_button.setEnabled(True)
        self.message_input.setEnabled(True)
        self.message_input.setFocus()

    def show_ai_response(self, text):
        self.add_message(text, is_user=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec_())