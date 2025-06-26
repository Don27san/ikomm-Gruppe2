\
import socket
import threading
import time
from protobuf import messenger_pb2
from config import config

# Placeholder for server details, ideally discovered or configured
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = config['chat_feature']['server_port']  # Use config port

class ChatClient:
    def __init__(self, user_id, server_id, server_host=DEFAULT_SERVER_HOST, server_port=DEFAULT_SERVER_PORT):
        self.user_id = user_id
        self.server_id = server_id  # User's homeserver
        self.server_host = server_host
        self.server_port = server_port
        self.sock = None
        self.is_connected = False
        self._message_counter = 0
        self._connect()

    def _connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))
            self.is_connected = True
            print(f"ChatClient: Connected to server {self.server_host}:{self.server_port}")
            # Start a thread to listen for incoming messages
            threading.Thread(target=self._listen_for_messages, daemon=True).start()
        except ConnectionRefusedError:
            print(f"ChatClient: Connection refused by server {self.server_host}:{self.server_port}")
            self.sock = None
            self.is_connected = False
        except Exception as e:
            print(f"ChatClient: Error connecting to server: {e}")
            self.sock = None
            self.is_connected = False

    def _ensure_connection(self):
        if not self.is_connected or self.sock is None:
            print("ChatClient: Not connected. Attempting to reconnect...")
            self._connect()
        return self.is_connected

    def _generate_snowflake(self):
        """Generate a simple snowflake ID"""
        self._message_counter += 1
        return int(time.time() * 1000) + self._message_counter

    def send_message_to_user(self, text_content, recipient_user_id, recipient_server_id):
        """Send a message to a specific user"""
        return self._send_chat_message(
            text_content=text_content,
            recipient_user_id=recipient_user_id,
            recipient_server_id=recipient_server_id
        )

    def send_message_to_group(self, text_content, recipient_group_id, recipient_server_id):
        """Send a message to a group"""
        return self._send_chat_message(
            text_content=text_content,
            recipient_group_id=recipient_group_id,
            recipient_server_id=recipient_server_id
        )

    def send_live_location(self, live_location, recipient_user_id=None, recipient_group_id=None, recipient_server_id=None):
        """Send a live location message"""
        return self._send_chat_message(
            live_location=live_location,
            recipient_user_id=recipient_user_id,
            recipient_group_id=recipient_group_id,
            recipient_server_id=recipient_server_id
        )

    def _send_chat_message(self, text_content=None, live_location=None, recipient_user_id=None, recipient_group_id=None, recipient_server_id=None):
        if not self._ensure_connection():
            print("ChatClient: Cannot send message. No connection to server.")
            return False

        chat_msg = messenger_pb2.ChatMessage()
        chat_msg.messageSnowflake = self._generate_snowflake()
        
        chat_msg.author.userId = self.user_id
        chat_msg.author.serverId = self.server_id

        # Set recipient
        if recipient_user_id and recipient_server_id:
            chat_msg.user.userId = recipient_user_id
            chat_msg.user.serverId = recipient_server_id
        elif recipient_group_id and recipient_server_id:
            chat_msg.group.groupId = recipient_group_id
            chat_msg.group.serverId = recipient_server_id
        else:
            print("ChatClient: Invalid recipient. Must specify user or group with their server ID.")
            return False

        # Set content
        if text_content:
            chat_msg.textContent = text_content
        elif live_location:
            chat_msg.live_location.CopyFrom(live_location)
        else:
            print("ChatClient: No content specified.")
            return False

        try:
            serialized_msg = chat_msg.SerializeToString()
            # Simple framing: send length of message first, then message
            msg_len = len(serialized_msg).to_bytes(4, 'big')
            self.sock.sendall(msg_len + serialized_msg)
            
            content_desc = text_content if text_content else "live location"
            recipient_desc = recipient_user_id or recipient_group_id
            print(f"ChatClient: Sent {content_desc} to {recipient_desc}@{recipient_server_id}")
            return True
        except Exception as e:
            print(f"ChatClient: Error sending message: {e}")
            self.is_connected = False
            self.sock.close()
            self.sock = None
            return False

    def _listen_for_messages(self):
        """Listen for incoming messages and responses"""
        while self.is_connected and self.sock:
            try:
                # Read message length
                msg_len_bytes = self.sock.recv(4)
                if not msg_len_bytes:
                    print("ChatClient: Server closed connection.")
                    self.is_connected = False
                    break
                
                msg_len = int.from_bytes(msg_len_bytes, 'big')
                if msg_len == 0:
                    continue

                # Read message data
                serialized_msg = b''
                while len(serialized_msg) < msg_len:
                    chunk = self.sock.recv(msg_len - len(serialized_msg))
                    if not chunk:
                        print("ChatClient: Incomplete message received.")
                        self.is_connected = False
                        return
                    serialized_msg += chunk

                # Try to parse as ChatMessage first
                try:
                    chat_msg = messenger_pb2.ChatMessage()
                    chat_msg.ParseFromString(serialized_msg)
                    self._handle_incoming_message(chat_msg)
                    continue
                except:
                    pass

                # Try to parse as ChatMessageResponse
                try:
                    response = messenger_pb2.ChatMessageResponse()
                    response.ParseFromString(serialized_msg)
                    self._handle_message_response(response)
                    continue
                except:
                    pass

                print(f"ChatClient: Received unrecognized message type")

            except Exception as e:
                print(f"ChatClient: Error listening for messages: {e}")
                self.is_connected = False
                break
        
        if self.sock:
            self.sock.close()
        self.sock = None
        self.is_connected = False
        print("ChatClient: Listener stopped.")

    def _handle_incoming_message(self, chat_msg):
        """Handle incoming ChatMessage"""
        content_type = chat_msg.WhichOneof('content')
        
        print(f"\n[INCOMING MESSAGE]")
        print(f"  From: {chat_msg.author.userId}@{chat_msg.author.serverId}")
        print(f"  Snowflake: {chat_msg.messageSnowflake}")
        
        if content_type == 'textContent':
            print(f"  Text: {chat_msg.textContent}")
        elif content_type == 'live_location':
            loc = chat_msg.live_location
            print(f"  Live Location: {loc.location.latitude}, {loc.location.longitude}")
            print(f"    From: {loc.user.userId}@{loc.user.serverId}")
        
        print()

    def _handle_message_response(self, response):
        """Handle ChatMessageResponse"""
        print(f"\n[MESSAGE RESPONSE]")
        print(f"  Snowflake: {response.messageSnowflake}")
        print(f"  Delivery statuses:")
        
        for status in response.statuses:
            status_name = messenger_pb2.ChatMessageResponse.Status.Name(status.status)
            print(f"    {status.user.userId}@{status.user.serverId}: {status_name}")
        print()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        self.is_connected = False
        print("ChatClient: Connection closed.")

if __name__ == '__main__':
    # Example Usage (for testing client/chat.py directly)
    my_user_id = "user123"
    my_server_id = "homeserver1"
    
    chat_client = ChatClient(user_id=my_user_id, server_id=my_server_id)

    if chat_client.is_connected:
        # Send a message to a user on another server
        chat_client.send_message_to_user(
            text_content="Hello UserX from User123!",
            recipient_user_id="userX",
            recipient_server_id="otherserver"
        )
        time.sleep(1)
        
        # Send a message to a group on a specific server
        chat_client.send_message_to_group(
            text_content="Hi GroupY!",
            recipient_group_id="groupY",
            recipient_server_id="homeserver1"
        )
        time.sleep(1)
        
        # Example of sending live location (create a sample location)
        live_location = messenger_pb2.LiveLocation()
        live_location.user.userId = my_user_id
        live_location.user.serverId = my_server_id
        live_location.timestamp = time.time()
        live_location.expiry_at = time.time() + 3600  # Expires in 1 hour
        live_location.location.latitude = 48.2627  # Munich
        live_location.location.longitude = 11.6742
        
        chat_client.send_live_location(
            live_location=live_location,
            recipient_user_id="userX",
            recipient_server_id="otherserver"
        )
        
        # Keep the client running to receive messages
        print("ChatClient: Running... Press Ctrl+C to exit")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nChatClient: Shutting down...")
        finally:
            chat_client.close()
    else:
        print("Failed to connect to chat server.")
