from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from GUI.locationviewer import LocationViewer
from PyQt5.QtCore import QThread, pyqtSignal
import os
import geocoder
import time

from client.typing_feature import TypingFeature
from client.location_feature import LocationFeature
from client.chat import ChatClient
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


class ChatListenerThread(QThread):
    message_received = pyqtSignal(dict)  # Emit message data

    def __init__(self, chat_client):
        super().__init__()
        self.chat_client = chat_client
        self.running = True

    def run(self):
        # Override the chat client's message handler to emit signals for GUI
        original_handler = self.chat_client._handle_incoming_message
        
        def gui_message_handler(chat_msg):
            # Convert protobuf message to dict for GUI
            content_type = chat_msg.WhichOneof('content')
            message_data = {
                'author': f"{chat_msg.author.userId}@{chat_msg.author.serverId}",
                'snowflake': chat_msg.messageSnowflake,
                'content_type': content_type
            }
            
            if content_type == 'textContent':
                message_data['text'] = chat_msg.textContent
            elif content_type == 'live_location':
                loc = chat_msg.live_location
                message_data['location'] = {
                    'latitude': loc.location.latitude,
                    'longitude': loc.location.longitude,
                    'user': f"{loc.user.userId}@{loc.user.serverId}",
                    'timestamp': loc.timestamp,
                    'expiry_at': loc.expiry_at
                }
            
            self.message_received.emit(message_data)
            # Still call original handler for console output
            original_handler(chat_msg)
        
        # Replace the message handler
        self.chat_client._handle_incoming_message = gui_message_handler
        
        # Keep thread alive while chat client is connected
        while self.running and self.chat_client.is_connected:
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class ChatWindow(QMainWindow):
    def __init__(self, typing_feature, location_feature, chat_client):
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

        # Initialize ChatClient instance
        self.chat_client = chat_client

        # Start chat listener thread
        if self.chat_client and self.chat_client.is_connected:
            self.chatListener = ChatListenerThread(self.chat_client)
            self.chatListener.message_received.connect(self.displayIncomingMessage)
            self.chatListener.start()
        else:
            self.chatListener = None
            self.chatDisplay.append("[System] Chat client not connected to server.")

        # Initialize current recipient (fixed values for simplicity)
        self.current_recipient_user = "friend_user"  # Fixed recipient
        self.current_recipient_server = "homeserver1"  # Fixed server

        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(2000)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.showTyping)
        self.sendButton.clicked.connect(self.sendMessage)
        self.shareLocationButton.clicked.connect(self.shareLocation)
        self.chatDisplay.anchorClicked.connect(self.handleLinkClick)

        self.typingLabel.clear()

        # Simple initialization message
        self.updateConnectionStatus()
        self.chatDisplay.append(f"[System] Sending messages to: {self.current_recipient_user}@{self.current_recipient_server}")

    def updateConnectionStatus(self):
        """Update the chat display with current connection status"""
        if self.chat_client and self.chat_client.is_connected:
            self.chatDisplay.append(f"[System] ✅ Connected as {self.chat_client.user_id}@{self.chat_client.server_id}")
        else:
            self.chatDisplay.append("[System] ❌ Not connected to chat server")

    def sendTypingEvent(self):
        self.typing_feature.send_typing_event()
        self.showTyping()

    def sendMessage(self):
        text = self.messageInput.text().strip()
        if text and self.chat_client and self.chat_client.is_connected:
            success = self.chat_client.send_message_to_user(
                text_content=text,
                recipient_user_id=self.current_recipient_user,
                recipient_server_id=self.current_recipient_server
            )
            
            if success:
                # Display sent message in chat
                self.chatDisplay.append(f"[You] {text}")
                self.messageInput.clear()
            else:
                self.chatDisplay.append("[System] Failed to send message")
        elif not self.chat_client or not self.chat_client.is_connected:
            self.chatDisplay.append("[System] Chat client not connected")
        elif not text:
            self.chatDisplay.append("[System] Cannot send empty message")

    def displayIncomingMessage(self, message_data):
        """Display incoming message in chat window"""
        author = message_data['author']
        content_type = message_data['content_type']
        
        if content_type == 'textContent':
            text = message_data['text']
            self.chatDisplay.append(f"[{author}] {text}")
        else:
            # For non-text messages, just show a simple notification
            self.chatDisplay.append(f"[{author}] sent a {content_type} message")

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
        link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15"
        html = f'<a href="{link}">📍 Click to view location</a>'
        self.chatDisplay.append(f"[Friend] live location: {html}")

    def stopLocationSharing(self):
        self.locationFeature.stop_location_sharing()
        self.chatDisplay.append("[System] Location sharing stopped.")

    def closeEvent(self, event):
        # Gracefully stop threads when window is closed
        self.typingThread.stop()
        self.locationFeature.stop_location_sharing()

        if hasattr(self, 'chatListener') and self.chatListener:
            self.chatListener.stop()

        if hasattr(self, 'locationSharingThread'):
            self.locationSharingThread.quit()
            self.locationSharingThread.wait()

        if hasattr(self, 'locationListener'):
            self.locationListener.stop()
            self.locationListener.quit()
            self.locationListener.wait()

        # Close chat client connection
        if self.chat_client:
            self.chat_client.close()

        event.accept()
