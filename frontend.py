import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
)
from PyQt5.QtCore import Qt, QTimer

import socket
import Backend_to_Frontend as bTf
import Backend as be



class Network:
    # check nerwork connection status
    def is_connected():
        try:
            # Attempt to connect to a reliable server (Google's DNS server)
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NOVA - Modern Chatbot")
        self.setGeometry(200, 100, 900, 650)

        # Modern Dark Theme with Gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #141e30, stop:1 #243b55
                );
                color: #ffffff;
                font-family: 'Poppins', sans-serif;
            }
            QTextEdit {
                background: rgba(40, 44, 52, 0.85);
                border: 2px solid #00aaff;
                border-radius: 12px;
                color: #e6e6e6;
                padding: 10px;
                font-size: 14pt;
            }
            QLineEdit {
                background: rgba(44, 49, 60, 0.85);
                border: 2px solid #00d1ff;
                border-radius: 12px;
                color: #ffffff;
                padding: 10px;
                font-size: 14pt;
            }
            QPushButton {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d2ff, stop:1 #3a7bd5
                );
                color: white;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                font: bold 14pt 'Poppins';
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QPushButton:hover {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3a7bd5, stop:1 #00d2ff
                );
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
            QLabel {
                font: bold 18pt 'Poppins';
                color: #00f7ff;
            }
        """)

        self.initUI()

    def initUI(self):
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Top Section: AI Name and Logo
        top_section = QHBoxLayout()

        # AI Name and Logo
        ai_name_logo = QLabel("🤖 NOVA")
        ai_name_logo.setAlignment(Qt.AlignLeft)
        ai_name_logo.setStyleSheet("font-size: 24pt; color: #00f7ff;")
        top_section.addWidget(ai_name_logo)

        # Spacer for alignment
        top_section.addStretch(1)

        # Internet Signal Status
        self.internet_status = QLabel("Checking internet status...")
        self.internet_status.setStyleSheet("color: #ffbf00; font-size: 12pt;")
        top_section.addWidget(self.internet_status)

        main_layout.addLayout(top_section)

        # Timer to update network status
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)  # Check every 2 seconds

        self.update_status()

        # Chat Area
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        main_layout.addWidget(self.chat_history)

        # Bottom Section: Speak, Mic, Input Field, and Send Button
        bottom_section = QHBoxLayout()

        # Speak Button
        self.speak_button = QPushButton("🔉SPEAK")
        self.speak_button.setFixedSize(160, 50)
        self.speak_button.clicked.connect(self.speak_action)
        bottom_section.addWidget(self.speak_button)

        # Mic Button
        self.mic_button = QPushButton("🎤 Mic")
        self.mic_button.setFixedSize(160, 50)
        self.mic_button.clicked.connect(self.toggle_mic)
        bottom_section.addWidget(self.mic_button)

        # Message input field
        # def message_input(self):
        #     self.message_input = QLineEdit()
        #     self.message_input.setPlaceholderText("Type your message here...")
        #     self.message_input.setMinimumHeight(70)
        #     bottom_section.addWidget(self.message_input, 1)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setMinimumHeight(70)
        bottom_section.addWidget(self.message_input, 1)
        # message_input(self)
        # Send Button
        self.send_button = QPushButton("⬆️SEND")
        self.send_button.setFixedSize(160, 50)
        self.send_button.clicked.connect(self.send_message)
        bottom_section.addWidget(self.send_button)

        main_layout.addLayout(bottom_section)
        self.setLayout(main_layout)

    def update_status(self):
        if Network.is_connected():
            self.internet_status.setText("Internet: Connected")
            self.internet_status.setStyleSheet("color: #38f000; font-size: 12pt;")
        else:
            self.internet_status.setText("Internet: Disconnected")
            self.internet_status.setStyleSheet("color: #f00000; font-size: 12pt;")

    def speak_action(self):
        self.chat_history.append("<i>Listening... (Simulated Speech Recognition)</i>")
        QTimer.singleShot(3000, self.show_speech_result)

    def show_speech_result(self):
        
        result=be.Backend.lisen(self)
        if result == None:
            self.chat_history.append("Nova: Sorry, I didn't get that.")
            return
        self.chat_history.append("You: "+ str(result))
        respondd=bTf.respond.send_message_to(self,result)
        be.Backend.speak(respondd)

    def toggle_mic(self):
        if self.mic_button.text() == "🎤 Mic":
            self.mic_button.setText("🔴 Listening...")
            self.mic_button.setStyleSheet("background: #d65b3e;")
            # result=be.Backend.lisen(self)
            # if result is None:
            #     self.chat_history.append("Nova: Sorry, I didn't get that.")
            #     return
            # self.chat_history.append("You: "+ str(result))
            # respondd=bTf.respond.send_message_to(self,result)
            # be.Backend.speak(respondd)

        else:
            self.mic_button.setText("🎤 Mic")
            self.mic_button.setStyleSheet("background: qlineargradient(stop:0 #00d2ff, stop:1 #3a7bd5);")




    # this function is used to send the message to the AI
    def send_message(self):
        
        # Send the message to the AI
        

        user_text = self.message_input.text()
        if user_text == None or user_text == "":
            None
        else:
            self.chat_history.append(f"You: {user_text}")
            # Clear the input field
            self.message_input.clear()
            bTf.respond.send_message_to(self,user_text)
            
        # return the user Query
        # else :
        #     self.chat_history.append(f"Nova: {user_text}")
        #     user_text = self.message_input.text()
        #     self.chat_history.append(f"You: {user_text}")
        #     self.message_input.clear()
        #     return user_text    

        

        
    def show_ai_response(self, message):
        self.chat_history.append(f"Nova: {message}")


if __name__ == "__main__":
     
    try:
        app = QApplication(sys.argv)
        chatbot = ChatBotApp()
        chatbot.show()
        sys.exit(app.exec_())
    except ModuleNotFoundError as e:
        print("Error:", e)
        print("It seems PyQt5 is not installed. Please install it using 'pip install PyQt5' and try again.")
