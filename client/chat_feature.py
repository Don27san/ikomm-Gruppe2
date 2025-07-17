from .feature_base import FeatureBase
from utils import serialize_msg, green, red, yellow, generate_chat_message
from protobuf import messenger_pb2
import time
import queue
from config import config
from PyQt5.QtCore import QObject, pyqtSignal
from google.protobuf.json_format import MessageToDict

class ChatFeature(FeatureBase, QObject):
    # Signal to emit when chat history is updated
    chatEventReceived = pyqtSignal()  # Trigger signal for GUI to refresh from chat_history
    def __init__(self):
        super().__init__('MESSAGES')
        QObject.__init__(self)
        self.chat_history = []
        self.ack_list = []

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
            self.chat_history.append(MessageToDict(message))
            self.chatEventReceived.emit()
            
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
            
            # Emit trigger signal for GUI to update from chat_history
            self.chatEventReceived.emit()

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
