\
import socket
import threading
import time
from protobuf import messenger_pb2 # Assuming your compiled protobuf file is here

# Placeholder for server details, ideally discovered or configured
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 6000 # Assuming a different port for TCP chat

class ChatClient:
    def __init__(self, user_id, server_id, server_host=DEFAULT_SERVER_HOST, server_port=DEFAULT_SERVER_PORT):
        self.user_id = user_id
        self.server_id = server_id # User's homeserver
        self.server_host = server_host
        self.server_port = server_port
        self.sock = None
        self.is_connected = False
        self._connect()

    def _connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_host, self.server_port))
            self.is_connected = True
            print(f"ChatClient: Connected to server {self.server_host}:{self.server_port}")
            # Optional: Start a thread to listen for incoming messages from the server if needed
            # threading.Thread(target=self._listen_for_messages, daemon=True).start()
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

    def send_chat_message(self, text_content, recipient_user_id=None, recipient_group_id=None, recipient_server_id=None):
        if not self._ensure_connection():
            print("ChatClient: Cannot send message. No connection to server.")
            return

        chat_msg = messenger_pb2.ChatMessage()
        chat_msg.messageSnowflake = int(time.time() * 1000) # Example snowflake
        
        chat_msg.author.userId = self.user_id
        chat_msg.author.serverId = self.server_id

        if recipient_user_id and recipient_server_id:
            chat_msg.recipient.user.userId = recipient_user_id
            chat_msg.recipient.user.serverId = recipient_server_id
        elif recipient_group_id and recipient_server_id:
            chat_msg.recipient.group.groupId = recipient_group_id
            chat_msg.recipient.group.serverId = recipient_server_id
        else:
            print("ChatClient: Invalid recipient. Must specify user or group with their server ID.")
            return

        chat_msg.textContent = text_content

        try:
            serialized_msg = chat_msg.SerializeToString()
            # Simple framing: send length of message first, then message
            msg_len = len(serialized_msg).to_bytes(4, 'big')
            self.sock.sendall(msg_len + serialized_msg)
            print(f"ChatClient: Sent message: {text_content} to {recipient_user_id or recipient_group_id}")
        except Exception as e:
            print(f"ChatClient: Error sending message: {e}")
            self.is_connected = False # Assume connection is lost on error
            self.sock.close()
            self.sock = None

    # def _listen_for_messages(self):
    #     # Basic listening logic if client needs to receive direct TCP messages
    #     # This would typically be for messages relayed by its homeserver
    #     while self.is_connected and self.sock:
    #         try:
    #             # Implement message receiving and deserialization (e.g., with length prefix)
    #             # For now, just a placeholder
    #             data = self.sock.recv(1024) 
    #             if not data:
    #                 print("ChatClient: Server closed connection.")
    #                 self.is_connected = False
    #                 break
    #             # Process received data (deserialize ChatMessage, etc.)
    #             print(f"ChatClient: Received data (raw): {data}")
    #         except Exception as e:
    #             print(f"ChatClient: Error listening for messages: {e}")
    #             self.is_connected = False
    #             break
    #     if self.sock:
    #         self.sock.close()
    #     self.sock = None
    #     self.is_connected = False
    #     print("ChatClient: Listener stopped.")

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
        self.is_connected = False
        print("ChatClient: Connection closed.")

if __name__ == '__main__':
    # Example Usage (for testing client/chat.py directly)
    # This would typically be integrated into client/main.py
    my_user_id = "user123"
    my_server_id = "homeserver1"
    
    chat_client = ChatClient(user_id=my_user_id, server_id=my_server_id)

    if chat_client.is_connected:
        # Send a message to a user on another server
        chat_client.send_chat_message(
            text_content="Hello UserX from User123!",
            recipient_user_id="userX",
            recipient_server_id="otherserver"
        )
        time.sleep(1)
        # Send a message to a group on a specific server
        chat_client.send_chat_message(
            text_content="Hi GroupY!",
            recipient_group_id="groupY",
            recipient_server_id="groupserver"
        )
        time.sleep(1)
        chat_client.close()
    else:
        print("Failed to connect to chat server.")
