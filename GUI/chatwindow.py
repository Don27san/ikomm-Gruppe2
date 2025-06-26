from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import uic

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("chatwindow.ui", self)

        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(2000)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.showTyping)
        self.sendButton.clicked.connect(self.sendMessage)
        self.shareLocationButton.clicked.connect(self.shareLocation)

        self.typingLabel.clear()

    def sendMessage(self):
        text = self.messageInput.text().strip()
        if text:
            self.chatDisplay.append("[You] " + text)
            self.messageInput.clear()
            self.chatDisplay.append("[Friend] reply test")

    def showTyping(self):
        self.typingLabel.setText("writing")
        self.typingTimer.start()

    def clearTyping(self):
        self.typingLabel.clear()

    def shareLocation(self):
        lat, lon = 52.52, 13.4050  # 示例位置，可替换为动态值
        link = f"https://www.google.com/maps?q={lat},{lon}"
        html = f'<a href="{link}">location</a>'
        self.chatDisplay.append(f"[You] location: {html}")
