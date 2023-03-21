import sys
import openai
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QScrollArea, QListWidget, QListWidgetItem
from PyQt6.QtGui import QAction

openai.api_key = "api_key"

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.chat_history = [{"role": "system", "content": "You are ChatGPT, an AI trained to assist users."}]

    def init_ui(self):
        self.setWindowTitle("ChatGPT Messaging")
        self.setGeometry(100, 100, 400, 600)

        self.layout = QVBoxLayout()

        self.message_area = QScrollArea()
        self.message_area.setWidgetResizable(True)
        self.layout.addWidget(self.message_area)

        self.chat_list = QListWidget()
        self.message_area.setWidget(self.chat_list)

        self.message_input = QLineEdit()
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def send_message(self):
        user_message = self.message_input.text()
        user_chat = {"role": "user", "content": user_message}
        self.chat_history.append(user_chat)

        user_item = QListWidgetItem("You: " + user_message)
        self.chat_list.addItem(user_item)

        self.message_input.clear()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            temperature=0.8,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        gpt_response = response['choices'][0]['message']['content'].strip()
        ai_chat = {"role": "assistant", "content": gpt_response}
        self.chat_history.append(ai_chat)

        ai_item = QListWidgetItem("ChatGPT: " + gpt_response)
        self.chat_list.addItem(ai_item)
        self.chat_list.scrollToBottom()

def main():
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
