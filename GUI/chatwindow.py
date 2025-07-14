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
from client.document_feature import DocumentFeature
# from client.chat_feature iimport ChatFeature
from utils import parse_msg, colors  # For parsing received messages
from config import config



class LocationListenerThread(QThread):
    def __init__(self, locationFeature):
        super().__init__()
        self.locationFeature = locationFeature

    def run(self):
        # Use the existing handle_listening method from LocationFeature
        self.locationFeature.handle_listening()

    def stop(self):
        self.locationFeature._running = False

class LocationSharingThread(QThread):
    def __init__(self, location_feature):
        super().__init__()
        self.location_feature = location_feature

    def run(self):
        self.location_feature.start_location_sharing()


class ChatWindow(QMainWindow):
    log_signal = pyqtSignal(str)

    def __init__(self, typing_feature, location_feature, chat_feature, translation, document):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "chatwindow.ui"), self)

        # Set window title with user info from config
        user_id = config['user']['userId']
        server_id = config['user']['serverId']
        self.setWindowTitle(f"Chat - {user_id}@{server_id}")

        # Initialize TypingFeature instance
        self.typing_feature = typing_feature

        # Initialize ChatFeature instance
        self.chat_feature = chat_feature
        # Connect chat history update signal to GUI refresh
        self.chat_feature.chatEventReceived.connect(self.updateChatDisplay)
        # Connect typing event receival signal to GUI refresh
        self.typing_feature.typing_event_received.connect(self.showTyping)

        # Initialize LocationFeature instance
        self.locationFeature = location_feature

        self.translationFeature = translation

        # Start background listener thread
        self.locationListener = LocationListenerThread(self.locationFeature)
        self.locationListener.start()
        # Connect the signal from LocationFeature directly to GUI
        self.locationFeature.locationEventReceived.connect(self.displayReceivedLocation)
        # track live-map viewer for continuous updates
        self.liveMapViewer = None  # will hold the map window for live updates

        self.typingTimer = QTimer(self)
        self.typingTimer.setInterval(1500)
        self.typingTimer.timeout.connect(self.clearTyping)

        self.messageInput.textEdited.connect(self.typing_feature.on_press)
        self.shareLocationButton.clicked.connect(self.shareLocation)
        self.chatDisplay.anchorClicked.connect(self.handleLinkClick)
        # disable default link navigation; handle clicks in handleLinkClick  
        self.chatDisplay.setOpenExternalLinks(False)
        self.chatDisplay.setOpenLinks(False)

        self.sendButton.clicked.connect(self.sendMessage)

        self.document_feature = document
        self.downloadButton.clicked.connect(self.downloadDocument)

        self.typingLabel.clear()

        self.log_signal.connect(self.status.append)
        colors.gui_logger = self.thread_safe_log
        
        # The chat feature connection is already handled in main.py
        # Load and display existing chat history when window opens
        self.updateChatDisplay()

    def updateChatDisplay(self):
        """Update chat display with all content from chat_history"""
        # Clear current display
        self.chatDisplay.clear()
        
        # Display all messages from chat_history
        for message in self.chat_feature.chat_history:
            formatted_content = self.formatChatMessage(message)
            self.chatDisplay.append(formatted_content)
    
    def formatChatMessage(self, message):
        """Format a chat message based on its content type"""
        # Handle dictionary message format with safe access
        try:
            author_info = message.get('author', {})
            user_id = author_info.get('userId', 'Unknown')
            server_id = author_info.get('serverId', 'Unknown')
            author = f"{user_id}@{server_id}"
        except (AttributeError, TypeError):
            author = "Unknown"
        
        # Check if message has textContent
        text_content = message.get('textContent', '')
        if text_content:
            return f"{author}: {text_content}"

        # Handle other content types if they exist
        document = message.get('document')
        if document:
            filename = document.get('filename', 'Unknown file')
            mime_type = document.get('mimeType', 'Unknown type')
            return f"{author}: 📄 {filename} ({mime_type})"
        
        live_location = message.get('live_location')
        if live_location:
            location = live_location.get('location', {})
            lat = location.get('latitude', 0.0)
            lon = location.get('longitude', 0.0)
            live_location_html = f'<a href="location://{lat},{lon}">Click to check the location</a>'
            return f"{author}: 📍 Location ({lat:.5f}, {lon:.5f}) - {live_location_html}"
        
        translation = message.get('translation')

        # Translation isn't used, it should be differently handled depending on the group
        if translation:
            lang_names = {0: 'DE', 1: 'EN', 2: 'ZH'}
            target_lang = translation.get('target_language', -1)
            lang_name = lang_names.get(target_lang, 'Unknown')
            original_msg = translation.get('original_message', '')
            return f"{author}: 🌐 Translation to {lang_name}: \"{original_msg}\""
        
        return f"{author}: [No content]"

    def thread_safe_log(self, text):
        self.log_signal.emit(text)


    def sendMessage(self):
        text = self.messageInput.text().strip()
        if text and self.recipientUserID() and self.recipientServerID():
            lang = self.chooseLanguage.currentText()
            emoji_to_code = {
                '🇨🇳': 'ZH',
                '🇬🇧': 'EN',
                '🇩🇪': 'DE',
            }
            if lang == 'choose language':
                self.chat_feature.send_message(
                    self.recipientUserID(),
                    self.recipientServerID(),
                    {'textContent': text}
                )
            elif lang in emoji_to_code:
                lang_code = emoji_to_code[lang]
                self.translationFeature.send_translation_request(
                    text, lang_code, self.recipientUserID(), self.recipientServerID()
                )   
            else:
                print(f"Unsupported language setting: {lang}")

            self.messageInput.clear()


        # if text:
        #     # send via chat_feature using recipient IDs
        #     self.chat_feature.send_message(
        #         self.recipientUserID(),
        #         self.recipientServerID(),
        #         text
        #     )
        #     self.messageInput.clear()
        #     # The sent message will be handled by the chat feature and appear in chat_history

    def showTyping(self, events_list=None):
        currently_typing = []
        for user in events_list:
            if time.time() - user.get('timestamp', 0) < 2:
                currently_typing.append(user['user']['userId'])
        
                
        
        self.typingLabel.setText(f"{', '.join(currently_typing)} {'are' if len(currently_typing) > 1 else 'is'} typing...")
        self.typingTimer.start()

    def clearTyping(self):
        self.typingLabel.clear()

    def shareLocation(self):
        g = geocoder.ip('me')
        if g.ok:
            lat, lon = g.latlng
            # open map viewer and update location
            if self.liveMapViewer is None:
                self.liveMapViewer = LocationViewer()
            self.liveMapViewer.show()
            self.liveMapViewer.updateLocation(lat, lon)
            
            # start background location-sharing
            self.locationSharingThread = LocationSharingThread(self.locationFeature)
            self.locationSharingThread.start()
        else:
            # Add system message to chat for error
            pass  # Could add error handling here if needed

    def handleLinkClick(self, url):
        # Handle location links with coordinates
        url_str = url.toString()
        if url_str.startswith("location://"):
            coords = url_str.replace("location://", "")
            try:
                lat, lon = map(float, coords.split(","))
                if self.liveMapViewer is None:
                    self.liveMapViewer = LocationViewer()
                self.liveMapViewer.show()
                self.liveMapViewer.updateLocation(lat, lon)
            except (ValueError, IndexError):
                print(f"Invalid location coordinates: {coords}")
        else:
            # Open the live map viewer (without reloading each time)
            if self.liveMapViewer is None:
                self.liveMapViewer = LocationViewer()
            self.liveMapViewer.show()

    def displayReceivedLocation(self, lat, lon):
        # Update the map marker; open map if needed
        # if self.liveMapViewer is None:
        #     self.liveMapViewer = LocationViewer()
        #     self.liveMapViewer.show()
        if self.liveMapViewer is not None:
            self.liveMapViewer.updateLocation(lat, lon)

    def stopLocationSharing(self):
        self.locationFeature.stop_location_sharing()
        self.chatDisplay.append("[System] Location sharing stopped.")

    def downloadDocument(self):
        self.document_feature.trigger_document_download(1234567890)
        

    def recipientUserID(self):
        UserID = self.recipient_user_id.text().strip()
        if UserID:
            return UserID
        else:
            return None
        
    def recipientServerID(self):
        ServerID = self.recipient_server_id.text().strip()
        if ServerID:
            return ServerID
        else:
            return None

    def closeEvent(self, event):
        # Gracefully stop threads when window is closed
        self.locationFeature.stop()
        self.typing_feature.stop()
        self.chat_feature.stop()
        self.document_feature.stop()
        #self.translation_feature.stop()

        event.accept()