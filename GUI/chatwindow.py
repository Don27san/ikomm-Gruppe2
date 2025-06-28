from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from GUI.locationviewer import LocationViewer
from PyQt5.QtCore import QThread, pyqtSignal
import os
import geocoder

from client.typing_feature import TypingFeature
from client.location_feature import LocationFeature
from utils import parse_msg  # For parsing received messages


# Thread for listening to TypingEvent
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
            self.typingEventReceived.emit()  # Notify UI

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class LocationListenerThread(QThread):
    location_received = pyqtSignal(float, float)  # lat, lon

    def __init__(self, locationFeature):
        super().__init__()
        self.locationFeature = locationFeature
        self.running = True

    def run(self):
        while self.running:
            res, addr = self.locationFeature.socket.recvfrom(1024)
            data = parse_msg(res)[2]
            if hasattr(data, 'location'):
                lat = data.location.latitude
                lon = data.location.longitude
                self.location_received.emit(lat, lon)

    def stop(self):
        self.running = False

class LocationSharingThread(QThread):
    def __init__(self, location_feature):
        super().__init__()
        self.location_feature = location_feature

    def run(self):
        self.location_feature.start_location_sharing()


class ChatWindow(QMainWindow):
    def __init__(self, typing_feature, location_feature):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "chatwindow.ui"), self)

        # Initialize TypingFeature instance
        self.typing_feature = typing_feature

        # Start background listener thread
        self.typingThread = TypingListenerThread(self.typing_feature)
        self.typingThread.typingEventReceived.connect(self.showTyping)
        self.typingThread.start()

        # Initialize LocationFeature instance
        self.locationFeature = location_feature

        # Start background listener thread
        self.locationListener = LocationListenerThread(self.locationFeature)
        self.locationListener.location_received.connect(self.displayReceivedLocation)
        self.locationListener.start()

        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(2000)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.showTyping)
        self.sendButton.clicked.connect(self.sendMessage)
        self.shareLocationButton.clicked.connect(self.shareLocation)
        self.chatDisplay.anchorClicked.connect(self.handleLinkClick)

        self.typingLabel.clear()

    def sendTypingEvent(self):
        self.typing_feature.send_typing_event()
        self.showTyping()

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
        g = geocoder.ip('me')
        if g.ok:
            lat, lon = g.latlng
            link = f"https://www.google.com/maps?q={lat},{lon}"
            html = f'<a href="{link}">Click to check the location</a>'
            self.chatDisplay.append(f"[You] live location: {html}")

            # Run location sharing in a separate thread
            self.locationSharingThread = LocationSharingThread(self.locationFeature)
            self.locationSharingThread.start()
        else:
            self.chatDisplay.append("[System] Could not get current location.")

    def handleLinkClick(self, url):
        self.viewer = LocationViewer(url.toString())
        self.viewer.show()

    def displayReceivedLocation(self, lat, lon):
        link = f"https://www.google.com/maps?q={lat},{lon}"
        html = f'<a href="{link}">Click to check the location</a>'
        self.chatDisplay.append(f"[Friend] live location: {html}")

    def stopLocationSharing(self):
        self.locationFeature.stop_location_sharing()
        self.chatDisplay.append("[System] Location sharing stopped.")

    def closeEvent(self, event):
        # Gracefully stop threads when window is closed
        self.typingThread.stop()
        self.locationFeature.stop_location_sharing()

        if hasattr(self, 'locationSharingThread'):
            self.locationSharingThread.quit()
            self.locationSharingThread.wait()

        if hasattr(self, 'locationListener'):
            self.locationListener.stop()
            self.locationListener.quit()
            self.locationListener.wait()

        event.accept()
