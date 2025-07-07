import time
import queue
from utils import green, red, serialize_msg, parse_msg, chat_message
from config import config
from .feature_base import FeatureBase
from protobuf import messenger_pb2

class ChatFeature(FeatureBase):
    """
    Chat feature that handles sending and receiving chat messages.
    Uses TCP connection for reliable message delivery.
    """

    def __init__(self):
        super().__init__('CHAT_MESSAGE')
        self.received_messages = []  # List to store received messages
        self.sent_messages = []      # List to store sent messages with status
        
        # Initialize for snowflake generation
        self._message_counter = 0
        self._user_hash = hash(chat_message.author.userId) & 0xFFFF

    def _generate_snowflake(self):
        """Generate a simple snowflake ID: timestamp + user_id + sequence"""
        # Get timestamp in milliseconds (42 bits)
        timestamp_ms = int(time.time() * 1000)
        
        # User hash (16 bits = 0-65535)
        user_hash = self._user_hash
        
        # Sequence counter (6 bits = 0-63)
        sequence = self._message_counter & 0x3F  # 6 bits
        self._message_counter += 1
        
        # Combine: [timestamp 42 bits][user_hash 16 bits][sequence 6 bits] = 64 bits total
        snowflake = (timestamp_ms << 22) | (user_hash << 6) | sequence
        
        return snowflake

    def send_text_message(self, recipient_user_id, recipient_server_id, text_content):
        """Send a text message to another user"""
        if not self._running or not hasattr(self, 'client') or self.client is None:
            red("Cannot send message: not connected to server")
            return False

        try:
            # Create chat message using new protobuf structure
            msg = messenger_pb2.ChatMessage()
            msg.messageSnowflake = self._generate_snowflake()
            
            # Set author
            msg.author.userId = chat_message.author.userId  # Use from payload
            msg.author.serverId = chat_message.author.serverId  # Use from payload
            
            # Set recipient
            msg.user.userId = recipient_user_id
            msg.user.serverId = recipient_server_id  
            
            # Set content
            msg.textContent = text_content

            # Send message
            serialized_msg = serialize_msg('CHAT_MESSAGE', msg)
            self.client.send_msg(serialized_msg)
            
            # Store sent message
            self.sent_messages.append({
                'messageSnowflake': msg.messageSnowflake,
                'timestamp': time.time(),
                'recipient': f"{recipient_user_id}@{recipient_server_id}",
                'textContent': text_content,
                'status': 'sent'
            })
            
            green(f"Text message sent to {recipient_user_id}@{recipient_server_id}: {text_content}")
            return True

        except Exception as e:
            red(f"Error sending text message: {e}")
            return False

    def handle_listening(self):
        """Handle incoming chat messages"""
        while self._running:
            if not hasattr(self, 'client') or self.client is None:
                time.sleep(0.1)
                continue
                
            try:
                msg, addr, _ = self.client.recv_msg()
                message_name, _, payload = parse_msg(msg)
                self.last_msg_received_time = time.time()
                
                if message_name == 'CHAT_MESSAGE':
                    self._handle_received_message(payload)
                    green(f'Received chat message from {addr[0]}:{addr[1]}')
                elif message_name == 'CHAT_MESSAGE_RESPONSE':
                    self._handle_message_response(payload)
                    green(f'Received message response from {addr[0]}:{addr[1]}')
                    
            except queue.Empty:
                if self._running:  # Only continue if still running
                    time.sleep(0.1)
                continue
            except Exception as e:
                if self._running:  # Only log if we're still supposed to be running
                    red(f"Error receiving chat message: {e}")
                time.sleep(0.1)

    def _handle_received_message(self, payload):
        """Handle an incoming chat message"""
        try:
            # Store received message
            received_msg = {
                'messageSnowflake': payload.get('messageSnowflake', 0),
                'timestamp': time.time(),
                'author': f"{payload.get('author', {}).get('userId', 'unknown')}@{payload.get('author', {}).get('serverId', 'unknown')}",
                'textContent': payload.get('textContent', ''),
                'received_at': time.time()
            }
            self.received_messages.append(received_msg)
            
            print(f"New message from {received_msg['author']}: {received_msg['textContent']}")
            
        except Exception as e:
            red(f"Error handling received message: {e}")

    def _handle_message_response(self, payload):
        """Handle a chat message response (delivery status)"""
        try:
            message_snowflake = payload.get('messageSnowflake', 0)
            statuses = payload.get('statuses', [])
            
            # Update sent message status
            for sent_msg in self.sent_messages:
                if sent_msg['messageSnowflake'] == message_snowflake:
                    sent_msg['delivery_status'] = statuses
                    break
                    
            print(f"Message {message_snowflake} delivery status: {statuses}")
            
        except Exception as e:
            red(f"Error handling message response: {e}")

    # Remove the old _generate_message_id method since we're using snowflakes now

    def get_received_messages(self):
        """Get all received messages"""
        return self.received_messages.copy()

    def get_sent_messages(self):
        """Get all sent messages"""
        return self.sent_messages.copy()

    def clear_messages(self):
        """Clear message history"""
        self.received_messages.clear()
        self.sent_messages.clear()
