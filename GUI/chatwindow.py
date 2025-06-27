from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from GUI.locationviewer import LocationViewer
from PyQt5.QtCore import QThread, pyqtSignal
import os

from client.typing_feature import TypingFeature  # 你之前的类
from utils import parse_msg  # 用于解析收到的消息


# 👂 监听 TypingEvent 的后台线程
class TypingListenerThread(QThread):
    typingEventReceived = pyqtSignal()

    def __init__(self, typing_feature):
        super().__init__()
        self.typing_feature = typing_feature
        self.running = True

    def run(self):
        while self.running:
            data, addr = self.typing_feature.socket.recvfrom(1024)
            parsed = parse_msg(data)
            self.typing_feature.event_list = parsed
            self.typingEventReceived.emit()  # 通知 UI

    def stop(self):
        self.running = False
        self.quit()
        self.wait()



class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "chatwindow.ui"), self)

        # 初始化 TypingFeature 实例
        self.typing_feature = TypingFeature()

        # 启动后台监听线程
        self.typingThread = TypingListenerThread(self.typing_feature)
        self.typingThread.typingEventReceived.connect(self.showTyping)
        self.typingThread.start()


        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(2000)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.showTyping)
        self.sendButton.clicked.connect(self.sendMessage)
        self.shareLocationButton.clicked.connect(self.shareLocation)
        self.chatDisplay.anchorClicked.connect(self.handleLinkClick)

        self.typingLabel.clear()

    def sendTypingEvent(self):
        self.typing_feature.send_typing_event()  # 👈 使用 TypingFeature 发事件
        self.showTyping()  # 本地也显示“writing”


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
        lat, lon = 52.52, 13.4050
        link = f"https://www.google.com/maps?q={lat},{lon}"
        html = f'<a href="{link}">klick to check the location</a>'
        self.chatDisplay.append(f"[You] live location: {html}")

    def handleLinkClick(self, url):
        self.viewer = LocationViewer(url.toString())
        self.viewer.show()

    def closeEvent(self, event):
        # 窗口关闭时优雅退出线程
        self.typingThread.stop()
        event.accept()
