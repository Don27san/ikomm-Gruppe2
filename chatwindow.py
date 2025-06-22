from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from locationviewer import LocationViewer
from client.typing_feature import TypingFeature
from client.location_feature import LocationFeature
from client.discovery_service import DiscoveryService
from client.connection_service import ConnectionService
from config import config
import threading

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("chatwindow.ui", self)

        # 网络连接
        discovery = DiscoveryService()
        servers = discovery.discover_servers()
        self.connector = ConnectionService(config['feature_support'], servers)
        self.connector.connect_client()

        # 功能模块绑定
        self.typingFeature = TypingFeature(self.connector)
        self.typingFeature.set_gui(self)

        self.locationFeature = LocationFeature(self.connector)
        self.locationFeature.set_gui(self)

        # GUI 控件连接
        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(2000)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.onTyping)
        self.sendButton.clicked.connect(self.sendMessage)
        self.shareLocationButton.clicked.connect(self.shareLocation)
        self.chatDisplay.anchorClicked.connect(self.handleLinkClick)

        self.typingLabel.clear()

        # 启动监听线程
        threading.Thread(target=self.typingFeature.handle_listening, daemon=True).start()
        threading.Thread(target=self.locationFeature.handle_listening, daemon=True).start()

    def sendMessage(self):
        text = self.messageInput.text().strip()
        if text:
            self.chatDisplay.append("[You] " + text)
            self.messageInput.clear()
            self.connector.send("message", {"text": text})

    def onTyping(self):
        self.typingLabel.setText("对方正在输入...")
        self.typingTimer.start()
        self.typingFeature.send_typing_event()

    def clearTyping(self):
        self.typingLabel.clear()

    def shareLocation(self):
        lat, lon = 52.52, 13.4050
        self.locationFeature.send_location(lat, lon)

    def show_location_popup(self, lat, lon):
        link = f"https://www.google.com/maps?q={lat},{lon}"
        self.viewer = LocationViewer(link)
        self.viewer.show()

    def handleLinkClick(self, url):
        self.viewer = LocationViewer(url.toString())
        self.viewer.show()

    def on_typing_received(self):
        self.typingLabel.setText("对方正在输入...")

    def on_location_received(self, lat, lon):
        self.show_location_popup(lat, lon)
