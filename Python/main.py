import os
import sys
import threading
from pathlib import Path
import geocoder
import time

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtCore import QObject, Signal, Slot, Property, QThread, QUrl, QTimer


# Import your existing backend
sys.path.append(str(Path(__file__).parent.parent))
from client.chat_feature import ChatFeature
from client.discovery_service import DiscoveryService
from client.document_feature import DocumentFeature
from client.location_feature import LocationFeature
from client.translation_feature import TranslationFeature
from client.typing_feature import TypingFeature
# from GUI.locationviewer import LocationViewer


from autogen.settings import url, import_paths


class LocationSharingThread(QThread):
    def __init__(self, location_feature, user_id, server_id):
        super().__init__()
        self.location_feature = location_feature
        self.user_id = user_id
        self.server_id = server_id

    def run(self):
        self.location_feature.start_location_sharing(self.user_id, self.server_id)

class ChatBackend(QObject):
    """Simple QObject to expose chat functionality to QML"""
    
    # Signals that QML can connect to
    messageReceived = Signal(str, str, str, str, str, bool)  # message, messageType, author, userinitials, color, isown
    contactAdded = Signal(str, str, str)
    locationReceived = Signal(float, float, str)  # latitude, longitude, authorName
    removeTypingMessage = Signal(str)  # author
    
    def __init__(self, engine):
        super().__init__()
        self.setup_backend()
        self.location_viewer_window = None
        self.location_component = None  # Store component reference
        self.engine = engine
        self.user_id = self.chat_feature.user_id
        self.server_id = self.chat_feature.server_id
        self.contact_id = f"{self.user_id}@{self.server_id}"

        self.typing_users = {}
        self.typingTimer = QTimer(self)
        self.typingTimer.start(300)
        self.typingTimer.timeout.connect(self.clearTyping)
        # Connect chat feature's messageReceived directly to QML
        if hasattr(self, 'chat_feature') and self.chat_feature:
            self.chat_feature.messageReceived.connect(self.messageReceived)
            self.chat_feature.contactAdded.connect(self.contactAdded)
        if hasattr(self, 'location_feature') and self.location_feature:
            self.location_feature.locationEventReceived.connect(self.locationReceived)
        if hasattr(self, 'typing_feature') and self.typing_feature:
            self.typing_feature.typing_event_received.connect(self.handleTypingEvent)

    def closeEvent(self, event):
        """Gracefully stop all features when window is closed"""
        print("Window closing, gracefully stopping all features...")
        
        # Stop all features in order
        try:
            self.locationFeature.stop()
            print("Location feature stopped")
        except Exception as e:
            print(f"Error stopping location feature: {e}")
            
        try:
            self.typing_feature.stop()
            print("Typing feature stopped")
        except Exception as e:
            print(f"Error stopping typing feature: {e}")
            
        try:
            self.chat_feature.stop()
            print("Chat feature stopped")
        except Exception as e:
            print(f"Error stopping chat feature: {e}")
            
        try:
            self.document_feature.stop()
            print("Document feature stopped")
        except Exception as e:
            print(f"Error stopping document feature: {e}")
            
        try:
            self.translation_feature.stop()
            print("Translation feature stopped")
        except Exception as e:
            print(f"Error stopping translation feature: {e}")
        
        print("All features stopped successfully")
        event.accept()  # Accept the close event

    def setup_backend(self):
        """Initialize your existing backend - same as your current main.py"""
        # Discover Servers
        discovery = DiscoveryService()
        server_list = discovery.discover_servers()

        # Initialize features
        self.typing_feature = TypingFeature()
        self.location_feature = LocationFeature()
        self.chat_feature = ChatFeature()
        self.translation_feature = TranslationFeature(chat_feature=self.chat_feature)
        self.document_feature = DocumentFeature()
        
        
        # Start threads (same as your current main.py)
        threading.Thread(target=self.typing_feature.handle_connection, args=(server_list,), daemon=True).start()
        threading.Thread(target=self.typing_feature.handle_listening, daemon=True).start()
        
        threading.Thread(target=self.location_feature.handle_connection, args=(server_list,), daemon=True).start()
        threading.Thread(target=self.location_feature.handle_listening, daemon=True).start()
        
        threading.Thread(target=self.chat_feature.handle_connection, args=(server_list,), daemon=True).start()
        threading.Thread(target=self.translation_feature.handle_connection, args=(server_list,), daemon=True).start()
        threading.Thread(target=self.document_feature.handle_connection, args=(server_list,), daemon=True).start()
    
    def handleTypingEvent(self, events_list):
        """Handle typing events from the TypingFeature"""
        current_time = time.time()
        for user in events_list:
            if current_time - user.get('timestamp', 0) < 1.5:
                author = f"{user['user']['userId']}@{user['user']['serverId']}"
                if author not in self.typing_users:
                    print(f"[Python] User started typing: {author}")
                    self.messageReceived.emit(
                        "",
                        "typing",
                        author,
                        self.chat_feature.get_contact_info(author)[0],
                        self.chat_feature.get_contact_info(author)[1],
                        False
                    )
                self.typing_users[author] = current_time
        

    def clearTyping(self):
        """Remove typing messages for users who stopped typing"""
        current_time = time.time()
        typing_timeout = 1.5 

        # Find users who should stop showing as typing
        users_to_remove = []
        for author, timestamp in self.typing_users.items():
            if current_time - timestamp > typing_timeout:
                users_to_remove.append(author)
        
        # Remove typing indicators for these users
        for author in users_to_remove:
            print(f"[Python] User stopped typing: {author}")
            self.removeTypingMessage.emit(author)
            del self.typing_users[author]

    @Property(str, constant=True)
    def myContactId(self):
        # Assuming self.chat_feature has user_id and server_id
        return self.contact_id

    @Slot(str, str, str)
    def sendMessage(self, contact_id, message, lang_code=""):
        """Slot that QML can call to send messages"""
        print(lang_code)
        if len(contact_id.split('@')) == 2:
            user_id, server_id = contact_id.split('@')
            if self.chat_feature:
                if lang_code == "":
                    self.chat_feature.send_message(user_id, server_id, {'textContent': message})
                else:
                    self.translation_feature.send_translation_request(
                    message, lang_code, user_id, server_id)
        else:
            print(f"Invalid contact ID format: {contact_id}")


    @Slot(str)
    def shareLocation(self, contact_id):
        """Share location with the specified contact (emit signal only)"""
        try:
            g = geocoder.ip('me')
            if '@' not in contact_id:
                print(f"Invalid contact ID format: {contact_id}")
                return
            recipient_user_id, recipient_server_id = contact_id.split('@')
            if g.ok and recipient_user_id and recipient_server_id:
                if (hasattr(self, 'locationSharingThread') and 
                    self.locationSharingThread is not None and 
                    self.locationSharingThread.isRunning() and
                    self.locationSharingThread.user_id == recipient_user_id and
                    self.locationSharingThread.server_id == recipient_server_id):
                    print(f"Already sharing location with user {contact_id}")
                    return
                lat, lon = g.latlng
                author = getattr(self.chat_feature, 'author', 'Unknown User')
                self.locationSharingThread = LocationSharingThread(
                    self.location_feature, 
                    recipient_user_id, 
                    recipient_server_id
                )
                self.locationSharingThread.start()
                print(f"Emitting locationReceived: {lat}, {lon}, {author}")
                self.chat_feature.chat_history.append({
                    'author': {
                        'userId': self.chat_feature.user_id,
                        'serverId': self.chat_feature.server_id
                    },
                    'user': {
                        'userId': recipient_user_id,
                        'serverId': recipient_server_id
                    },
                    ''
                    'liveLocation': {
                        'location': {
                            'latitude': lat,
                            'longitude': lon
                        },
                        'author': author
                    },
                    "expiry_at": 0,
                    "timestamp": 0,
                    "user": {
                        "userId": recipient_user_id,
                        "serverId": recipient_server_id
                    }
                })
                self.messageReceived.emit(
                    f"{lat}:{lon}",
                    "liveLocation",
                    contact_id,
                    self.chat_feature.get_contact_info(contact_id)[0],
                    self.chat_feature.get_contact_info(contact_id)[1],
                    True
                )
                self.locationReceived.emit(lat, lon, author)
            else:
                if not g.ok:
                    print(f"Failed to get location: {g.status}")
                else:
                    print("Invalid recipient user/server ID")
        except Exception as e:
            print(f"Error in shareLocation: {str(e)}")
            import traceback
            traceback.print_exc()


    # @Slot(str)
    # def shareLocation(self, contact_id):
    #     g = geocoder.ip('me')
    #     recipient_user_id, recipient_server_id = contact_id.split('@')
    #     if g.ok and recipient_user_id and recipient_server_id:
    #         lat, lon = g.latlng
            
    #         # Create location viewer window if it doesn't exist
    #         if not self.location_viewer_window:
    #             self.create_location_viewer()
            
    #         # if self.location_viewer_window:
    #             # Update location and show window
    #             # self.location_viewer_window.updateLocation(lat, lon, self.chat_feature.author)
    #             # self.location_viewer_window.showWindow()
            
    #         # Start background location-sharing
    #         self.locationSharingThread = LocationSharingThread(self.location_feature, recipient_user_id, recipient_server_id)
    #         self.locationSharingThread.start()
    #     else:
    #         print("Failed to get location or invalid contact ID")

    @Slot(str, str)
    def addContact(self, user_id, server_id):
        """Slot that QML can call to add contacts"""
        if self.chat_feature:
            self.chat_feature.add_contact(user_id, server_id)

    @Slot(str, result=str)
    def translateMessage(self, message):
        """Slot that QML can call to translate messages"""
        if self.translation_feature:
            return self.translation_feature.translate(message)
        return message
    
    @Slot(str)
    def contactClicked(self, contact_id):
        """Called from QML when a contact is clicked"""
        for message in self.chat_feature.get_messages(contact_id):
            isOwn = (message['author']['userId'] == self.chat_feature.user_id) and (message['author']['serverId'] == self.chat_feature.server_id)
            print(f"[Python] contactClicked: {contact_id} - {message}")
            if 'textContent' in message:
                messageType = "textContent"
                messageText = message['textContent']
            elif 'document' in message:
                messageType = "document"
                messageText = message['document'].get('fileName', 'Document')
            # elif 'translation' in message:
            #     messageType = "translation"
            #     messageText = message['translation'].translatedText if message['translation'].translatedText else "Translation"
            elif 'liveLocation' in message:
                messageType = "liveLocation"
                messageText = str(message['liveLocation'].get('location', {}).get('latitude', 'Unknown')) + ":" + str(message['liveLocation'].get('location', {}).get('longitude', 'Unknown'))
            else:
                messageType = "unknown"
                messageText = "Unknown Content"

            
            # Emit the messageReceived signal to QML
            self.messageReceived.emit(
                messageText,
                messageType,
                contact_id,
                self.chat_feature.get_contact_info(contact_id)[0],
                self.chat_feature.get_contact_info(contact_id)[1],
                isOwn
            )
        print(f"[Python] contactClicked received: {contact_id}")


    @Slot()
    def on_text_changed(self):
        """Called from QML when text in the input field changes"""
        if self.chat_feature:
            self.typing_feature.on_press("")

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Create your backend
    chat_backend = ChatBackend(engine)
    
    # Expose it to QML - this is the "bridge" (much simpler than I initially suggested)
    engine.rootContext().setContextProperty("chatBackend", chat_backend)

    app_dir = Path(__file__).parent.parent

    engine.addImportPath(os.fspath(app_dir))
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    engine.load(os.fspath(app_dir/url))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
