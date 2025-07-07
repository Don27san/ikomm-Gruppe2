import time
import queue
from protobuf import messenger_pb2
from config import config
from utils import blue, green, yellow, red, parse_msg, serialize_msg
from .service_base import ServiceBase

class ChatService(ServiceBase):
    """
    Chat service that handles chat messages between users.
    Manages message routing and delivery status reporting.
    """

    def __init__(self):
        super().__init__('CHAT_MESSAGE', bind_port=config['chat_feature']['server_connection_port'])
        self.server_id = "server456"  # This server's ID
        self.message_store = {}  # Store messages for delivery status tracking
        self.user_connections = {}  # Map user_id to connection info

    def handle_connections(self):
        """Override base handle_connections to include chat-specific message handling"""
        self.server = self._setup_server()
        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while self._running:
            self._check_clients_active()

            try:
                msg, addr, conn = self.server.recv_msg()
                message_name, _, data = parse_msg(msg)
                subscriberIP = addr[0]
            except queue.Empty:
                continue
            except Exception:
                continue

            # Update last active time for known clients
            if subscriberIP in self.subscriber_dict:
                self.subscriber_dict[subscriberIP]['lastActive'] = time.time()
                self.subscriber_dict[subscriberIP]['ping_sent'] = False

            # Handle chat-specific messages
            if message_name == 'CHAT_MESSAGE':
                self._handle_chat_message(subscriberIP, addr, conn, data)
            elif subscriberIP in self.subscriber_dict:
                # Handle standard service messages for known clients
                self._handle_known_client_message(subscriberIP, addr, conn, message_name, data)
            else:
                # Handle new client connection
                self._handle_new_client_connection(subscriberIP, addr, conn, message_name, data)

    def _setup_server(self):
        """Setup the server connection"""
        from utils import ConnectionHandler
        server = ConnectionHandler(timeout=self.ping_timeout)
        server.start_server(self.bind_ip, self.bind_port)
        return server

    def _check_clients_active(self):
        """Check if clients are still active and send pings if necessary"""
        if len(self.subscriber_dict) == 0:
            return
            
        for subscriberIP, data in list(self.subscriber_dict.items()):
            if time.time() - data['lastActive'] > self.ping_timeout and not data['ping_sent']:
                # Send ping
                from utils import ping
                try:
                    data['conn'].send(serialize_msg('PING', ping))
                    data['ping_sent'] = True
                    yellow(f"{self.feature_name}: Ping sent to {subscriberIP}")
                except Exception:
                    # Connection lost
                    del self.subscriber_dict[subscriberIP]
                    red(f"{self.feature_name}: Lost connection to {subscriberIP}")
            elif time.time() - data['lastActive'] > 2 * self.ping_timeout and data['ping_sent']:
                # Client timeout
                try:
                    data['conn'].close()
                except Exception:
                    pass
                del self.subscriber_dict[subscriberIP]
                red(f"{self.feature_name}: Client {subscriberIP} timed out")

    def _handle_known_client_message(self, subscriberIP, addr, conn, message_name, data):
        """Handle messages from known clients"""
        if message_name == 'CONNECT_CLIENT':
            response = messenger_pb2.ConnectResponse()
            response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
            conn.send(serialize_msg('CONNECTED', response))
            yellow(f"{self.feature_name}: {addr} already subscribed.")
        elif message_name == 'PING':
            from utils import pong
            conn.send(serialize_msg('PONG', pong))
            green(f"{self.feature_name}: Pong answered to {addr}")
        elif message_name == 'PONG':
            green(f"{self.feature_name}: Pong received from {addr}")
        elif message_name == 'HANGUP':
            user_id = self.subscriber_dict[subscriberIP].get('userId')
            if user_id and user_id in self.user_connections:
                del self.user_connections[user_id]
            del self.subscriber_dict[subscriberIP]
            conn.close()
            red(f"{self.feature_name}: Hangup received from {addr}. Connection closed.")
        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to {addr}")

    def _handle_new_client_connection(self, subscriberIP, addr, conn, message_name, data):
        """Handle connection from new client"""
        if message_name == 'CONNECT_CLIENT':
            # Store connection info
            data['conn'] = conn
            data['addr'] = addr
            data['lastActive'] = time.time()
            data['ping_sent'] = False
            
            # Extract user info
            user_info = data.get('user', {})
            user_id = user_info.get('userId', '')
            data['userId'] = user_id
            
            # Store user connection mapping
            if user_id:
                self.user_connections[user_id] = {
                    'subscriberIP': subscriberIP,
                    'conn': conn,
                    'addr': addr
                }
            
            self.subscriber_dict[subscriberIP] = data
            
            # Send success response
            response = messenger_pb2.ConnectResponse()
            response.result = messenger_pb2.ConnectResponse.Result.CONNECTED
            conn.send(serialize_msg('CONNECTED', response))
            green(f"{self.feature_name}: New client connected from {addr}")
        else:
            # Send error for unknown client with wrong first message
            try:
                unsupported_message = messenger_pb2.UnsupportedMessage()
                unsupported_message.message_name = message_name
                conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                conn.close()
            except Exception:
                pass
            yellow(f"{self.feature_name}: Unknown client {addr} sent {message_name}. Connection closed.")

    def _handle_chat_message(self, subscriberIP, addr, conn, payload):
        """Handle incoming chat message"""
        try:
            message_snowflake = payload.get('messageSnowflake', 0)
            author = payload.get('author', {})
            recipient = payload.get('user', {})
            text_content = payload.get('textContent', '')
            
            green(f"Chat message received: {message_snowflake} from {author.get('userId', 'unknown')}")
            
            # Store message for delivery tracking
            self.message_store[message_snowflake] = {
                'payload': payload,
                'sender_conn': conn,
                'sender_addr': addr,
                'timestamp': time.time()
            }
            
            # Route message to recipient
            recipient_user_id = recipient.get('userId', '')
            recipient_server_id = recipient.get('serverId', '')
            
            delivery_status = self._route_message(message_snowflake, payload, recipient_user_id, recipient_server_id)
            
            # Send delivery response back to sender
            self._send_message_response(conn, message_snowflake, delivery_status)
            
        except Exception as e:
            red(f"Error handling chat message: {e}")

    def _route_message(self, message_snowflake, payload, recipient_user_id, recipient_server_id):
        """Route message to recipient and return delivery status"""
        try:
            # Check if recipient is connected to this server
            if recipient_user_id in self.user_connections:
                # Local delivery
                recipient_conn_info = self.user_connections[recipient_user_id]
                recipient_conn = recipient_conn_info['conn']
                
                try:
                    # Forward message to recipient
                    chat_msg = messenger_pb2.ChatMessage()
                    chat_msg.messageSnowflake = payload.get('messageSnowflake', 0)
                    
                    # Copy author info
                    author_info = payload.get('author', {})
                    chat_msg.author.userId = author_info.get('userId', '')
                    chat_msg.author.serverId = author_info.get('serverId', '')
                    
                    # Copy recipient info  
                    chat_msg.user.userId = recipient_user_id
                    chat_msg.user.serverId = recipient_server_id
                    
                    # Copy content
                    chat_msg.textContent = payload.get('textContent', '')
                    
                    recipient_conn.send(serialize_msg('CHAT_MESSAGE', chat_msg))
                    green(f"Message {message_snowflake} delivered to local user {recipient_user_id}")
                    
                    return [{
                        'user': {'userId': recipient_user_id, 'serverId': recipient_server_id},
                        'status': 'DELIVERED'
                    }]
                    
                except Exception as e:
                    red(f"Error delivering message to local user: {e}")
                    return [{
                        'user': {'userId': recipient_user_id, 'serverId': recipient_server_id},
                        'status': 'OTHER_ERROR'
                    }]
            else:
                # User not found on this server
                yellow(f"User {recipient_user_id} not found on this server")
                return [{
                    'user': {'userId': recipient_user_id, 'serverId': recipient_server_id},
                    'status': 'USER_NOT_FOUND'
                }]
                
        except Exception as e:
            red(f"Error routing message: {e}")
            return [{
                'user': {'userId': recipient_user_id, 'serverId': recipient_server_id},
                'status': 'OTHER_ERROR'
            }]

    def _send_message_response(self, sender_conn, message_snowflake, delivery_statuses):
        """Send message delivery response back to sender"""
        try:
            # Create ChatMessageResponse using the new protobuf structure
            response = messenger_pb2.ChatMessageResponse()
            response.messageSnowflake = message_snowflake
            
            # Add delivery statuses
            for status_info in delivery_statuses:
                delivery_status = response.statuses.add()
                user_info = status_info.get('user', {})
                delivery_status.user.userId = user_info.get('userId', '')
                delivery_status.user.serverId = user_info.get('serverId', '')
                
                # Map string status to enum
                status_str = status_info.get('status', 'UNKNOWN_STATUS')
                if status_str == 'DELIVERED':
                    delivery_status.status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
                elif status_str == 'USER_NOT_FOUND':
                    delivery_status.status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
                elif status_str == 'USER_AWAY':
                    delivery_status.status = messenger_pb2.ChatMessageResponse.Status.USER_AWAY
                elif status_str == 'OTHER_ERROR':
                    delivery_status.status = messenger_pb2.ChatMessageResponse.Status.OTHER_ERROR
                else:
                    delivery_status.status = messenger_pb2.ChatMessageResponse.Status.UNKNOWN_STATUS
            
            sender_conn.send(serialize_msg('CHAT_MESSAGE_RESPONSE', response))
            
            green(f"Delivery response sent for message {message_snowflake}")
            
        except Exception as e:
            red(f"Error sending message response: {e}")

    def stop(self):
        """Gracefully stop the chat service"""
        self._running = False
        
        # Close all client connections
        for subscriberIP, data in list(self.subscriber_dict.items()):
            try:
                hangup = messenger_pb2.HangUp()
                hangup.reason = messenger_pb2.HangUp.Reason.EXIT
                conn = data['conn']
                conn.send(serialize_msg('HANGUP', hangup))
                conn.close()
            except Exception:
                pass
        
        red(f"{self.feature_name}: Service stopped. All connections closed.")
        
        if hasattr(self, 'server'):
            self.server.close()
