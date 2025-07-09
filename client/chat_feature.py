from .feature_base import FeatureBase
from utils import serialize_msg, parse_msg, green, red, yellow
from protobuf import messenger_pb2
import time
import queue
from config import config

class ChatFeature(FeatureBase):
    def __init__(self):
        super().__init__('CHAT_MESSAGE')
        self.chat_history = []
        self.ack_list = []

    def send_message(self, recipient_user_id, recipient_server_id, text):
        if not self._running or not self.client:
            red("Not connected to chat server.")
            return

        message = messenger_pb2.ChatMessage()
        # Generate a unique snowflake ID. Using time and random for simplicity.
        message.messageSnowflake = int(time.time() * 1000)
        message.author.userId = config['user']['userId']
        message.author.serverId = config['user']['serverId']
        message.textContent = text

        # Set the recipient
        recipient = message.user
        recipient.userId = recipient_user_id
        recipient.serverId = recipient_server_id

        try:
            self.client.send_msg(serialize_msg('CHAT_MESSAGE', message))
            yellow(f"Sent message: {text}")
        except Exception as e:
            red(f"Failed to send message: {e}")

    def handle_feature_message(self, message_name, payload, conn):
        if message_name == 'CHAT_MESSAGE':
            self.chat_history.append(payload)
            author_info = payload.get('author', {})
            user_id = author_info.get('userId', 'Unknown')
            server_id = author_info.get('serverId', 'Unknown')
            message_text = payload.get('textContent', '')
            green(f"Received message from @{user_id}@{server_id}: \"{message_text}\"")

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
