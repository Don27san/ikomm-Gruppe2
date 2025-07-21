from .feature_base import FeatureBase
from utils import serialize_msg, green, red, yellow, generate_chat_message
from protobuf import messenger_pb2
import time
import queue
from config import config
from PySide6.QtCore import QObject, Signal
from google.protobuf.json_format import MessageToDict

class ChatFeature(FeatureBase, QObject):
    # Signal to emit when a new message is sent or received
    messageReceived = Signal(str, str, str, str, str, bool)  # message, messageType, author, userinitials, color, isown
    contactAdded = Signal(str, str, str)  # contactId, userInitials, avatarColor
    def __init__(self):
        super().__init__('MESSAGES')
        QObject.__init__(self)
        self.chat_history = []
        self.ack_list = []
        self.contact_dict = {}
        self.user_id = config['user']['userId']
        self.server_id = config['user']['serverId']
        self.author = f"{self.user_id}@{self.server_id}"

    def get_contact_info(self, contact_id):
        """Retrieve contact information by contact_id, generating if missing."""
        if contact_id in self.contact_dict:
            return self.contact_dict[contact_id]['userInitials'], self.contact_dict[contact_id]['avatarColor']

        # If not found, parse user_id and server_id
        try:
            user_id, server_id = contact_id.split("@", 1)
        except Exception:
            user_id = contact_id
            server_id = ""

        # Generate user initials (first and last letter of user_id, capitalized)
        user_initials = f"{user_id[0].upper()}{user_id[-1].upper()}" if user_id else "?"
        # Generate a simple avatar color based on user_id
        colors = ["#afdeff", "#ffafaf", "#afffaf", "#ffdfaf", "#dfafff", "#afafff"]
        hash_value = 0
        for char in contact_id:
            hash_value = ((hash_value << 5) - hash_value) + ord(char)
            hash_value = hash_value & 0xFFFFFFFF  # Keep as 32-bit integer
        avatar_color = colors[abs(hash_value) % len(colors)]

        return user_initials, avatar_color

    def add_contact(self, user_id, server_id):
        """Add a contact to the contact_dict (dict-based storage)"""
        contact_id = f"{user_id}@{server_id}"
        # Check if contact already exists in contact_dict
        if contact_id in self.contact_dict:
            print(f"Contact {contact_id} already exists")
            # self.contactAdded.emit(
            #         contact_id,
            #         self.contact_dict[contact_id]['userInitials'],
            #         self.contact_dict[contact_id]['avatarColor']
            #     )
            return

        user_initials, avatar_color = self.get_contact_info(contact_id)

        contact = {
            'userId': user_id,
            'serverId': server_id,
            'userInitials': user_initials,
            'avatarColor': avatar_color,
            'timestamp': time.time(),
        }

        self.contact_dict[contact_id] = contact
        green(f"Added contact: {user_id}@{server_id}")
        self.contactAdded.emit(
                    contact_id,
                    self.contact_dict[contact_id]['userInitials'],
                    self.contact_dict[contact_id]['avatarColor']
                )
    
    def get_messages(self, contact_id):
        """Retrieve messages for a specific contact"""
        # Filter messages by contact_id
        print(self.chat_history)
        messages = [msg for msg in self.chat_history if (f"{msg.get('author', {}).get('userId', '')}@{msg.get('author', {}).get('serverId', '')}" == contact_id or f"{msg.get('user', {}).get('userId', '')}@{msg.get('user', {}).get('serverId', '')}" == contact_id)]
        return messages

    def send_message(self, recipient_user_id, recipient_server_id, content=None):
        if not self.is_connected():
            red("Not connected to chat server.")
            return

        # If no content is provided, default to text content
        if content is None:
            content = {'textContent': "Hello, this is a test message!"}

        # Use the generate_chat_message utility function
        message = generate_chat_message(
            author_user_id=config['user']['userId'],
            author_server_id=config['user']['serverId'],
            recipient={'user': {'userId': recipient_user_id, 'serverId': recipient_server_id}},
            content=content
        )

        try:
            self.client.send_msg(serialize_msg('MESSAGE', message))
            yellow(f"Sent message: {content}")
            # Add sent message to chat_history so it appears in GUI
            msg_dict = MessageToDict(message)
            self.chat_history.append(msg_dict)

            if 'textContent' in content:
                messageType = "textContent"
                messageText = content['textContent']
            elif 'document' in content:
                messageType = "document"
                messageText = content['document'].get('fileName', 'Document')
            # elif 'translation' in message:
            #     messageType = "translation"
            #     messageText = message['translation'].translatedText if message['translation'].translatedText else "Translation"
            elif 'live_location' in content:
                messageType = "live_location"
                messageText = content['live_location'].get('location', {}).get('latitude', 'Unknown') + ":" + content['live_location'].get('location', {}).get('longitude', 'Unknown')
            else:
                messageType = "unknown"
                messageText = "Unknown Content"
            # Emit signal for QML

            contact_id = f"{recipient_user_id}@{recipient_server_id}"
            self.messageReceived.emit(
                messageText,
                messageType,
                contact_id,
                self.get_contact_info(contact_id)[0],
                self.get_contact_info(contact_id)[1],
                True
            )
        except Exception as e:
            red(f"Failed to send message: {e}")

    def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
        if message_name == 'MESSAGE':
            self.chat_history.append(payload)
            author_info = payload.get('author', {})
            user_id = author_info.get('userId', 'Unknown')
            server_id = author_info.get('serverId', 'Unknown')
            message_text = payload.get('textContent', '')
            green(f"Received message from {user_id}@{server_id}: \"{message_text}\"")
            # Emit signal for QML
            contact_id = f"{user_id}@{server_id}"
        
        # Check if contact already exists
            self.add_contact(user_id, server_id)
            if 'textContent' in payload:
                messageType = "textContent"
                messageText = payload['textContent']
            elif 'document' in payload:
                messageType = "document"
                messageText = payload['document'].get('fileName', 'Document')
            # elif 'translation' in message:
            #     messageType = "translation"
            #     messageText = message['translation'].translatedText if message['translation'].translatedText else "Translation"
            elif 'liveLocation' in payload:
                messageType = "liveLocation"
                messageText = str(payload['liveLocation'].get('location', {}).get('latitude', 'Unknown')) + ":" + str(payload['liveLocation'].get('location', {}).get('longitude', 'Unknown'))
            else:
                messageType = "unknown"
                messageText = "Unknown Content"
            self.messageReceived.emit(messageText, messageType, f"{user_id}@{server_id}", self.get_contact_info(contact_id)[0], self.get_contact_info(contact_id)[1],False)
            # Acknowledge the message back to the server
            try:
                response = messenger_pb2.ChatMessageResponse()
                response.messageSnowflake = int(payload.get('messageSnowflake'))
                # In a real app, you'd identify the current user. Here, we just confirm delivery.
                delivery_status = response.statuses.add()
                delivery_status.status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
                conn.send_msg(serialize_msg('MESSAGE_ACK', response))
                yellow(f"Sent ACK for message {payload.get('messageSnowflake')}")
            except Exception as e:
                red(f"Failed to send ACK for message {payload.get('messageSnowflake')}: {e}")
            return True
        elif message_name == 'MESSAGE_ACK':
            self.ack_list.append(payload)
            green(f"Received ACK for message {payload.get('messageSnowflake')}")
            return True
        return False

    def stop(self):
        super().stop()
        green("Chat feature stopped.")
