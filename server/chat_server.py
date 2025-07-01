import socket
import threading
import time
from protobuf import messenger_pb2
from config import config
from utils import ConnectionHandler, parse_msg, serialize_msg, red, green, yellow, blue
from .service_base import ServiceBase

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = config['chat_feature']['server_port']  # Port for TCP chat service
SERVER_ID = "homeserver1"  # This server's unique ID

class ChatService(ServiceBase):
    """
    Chat service that handles chat messages between users and groups.
    Uses ServiceBase for connection management and standard message handling.
    """
    
    def __init__(self):
        super().__init__('CHAT_MESSAGE', bind_port=PORT)
        self.server_id = SERVER_ID
        
        # In-memory storage for connected clients and server/group info
        self.connected_clients = {}  # { user_id: connection_info }
        self.server_directory = {}  # { "server_id": ("host", port) }
        self.group_members = {}  # { ("group_id", "group_server_id"): [("user_id", "user_server_id")] }
        
        # Initialize some example group members for testing
        self.group_members[("groupY", "homeserver1")] = [("user123", "homeserver1"), ("user456", "homeserver1")]
        self.group_members[("groupY", "homeserver1")].extend([("user1", "homeserver1"), ("user2", "homeserver1")])

    def handle_connections(self):
        """Override to handle chat-specific message processing"""
        server = ConnectionHandler(timeout=self.ping_timeout)
        server.start_server(self.bind_ip, self.bind_port)

        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while True:
            # Check: client still active
            self._check_clients_active()

            try:
                msg, addr, conn = server.recv_msg()
                message_name, _, data = parse_msg(msg)
                subscriberIP = addr[0]
            except Exception as e:
                continue

            # Handle CHAT_MESSAGE specifically, delegate other messages to ServiceBase logic
            if message_name == 'CHAT_MESSAGE':
                self._handle_chat_message(subscriberIP, addr, conn, data)
            else:
                # Use ServiceBase's standard message handling for CONNECT_CLIENT, PING, PONG, etc.
                self._handle_standard_messages(message_name, subscriberIP, addr, conn, data)

    def _handle_standard_messages(self, message_name, subscriberIP, addr, conn, data):
        """Handle standard ServiceBase messages (CONNECT_CLIENT, PING, PONG, etc.)"""
        # Known client handling
        if subscriberIP in self.subscriber_dict.keys():
            # update data
            self.subscriber_dict[subscriberIP]['lastActive'] = time.time()
            self.subscriber_dict[subscriberIP]['ping_sent'] = False
            # handle received message
            if message_name == 'CONNECT_CLIENT':
                response = messenger_pb2.ConnectionResponse()
                response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
                response.udpPort = self.forwarding_port
                conn.send(serialize_msg('CONNECTION_RESPONSE', response))
                yellow(f"{self.feature_name}: {addr} already subscribed. \n")
            elif message_name == 'PING':
                from utils import pong
                conn.send(serialize_msg('PONG', pong))
                green(f"{self.feature_name}: Pong answered to {addr}. \n")
            elif message_name == 'PONG':
                green(f"{self.feature_name}: Pong received from {addr} \n")
            elif message_name == 'HANGUP':
                del self.subscriber_dict[subscriberIP]
                # Also remove from connected_clients
                for user_id, client_info in list(self.connected_clients.items()):
                    if client_info.get('addr') == addr:
                        del self.connected_clients[user_id]
                        break
                conn.close()
                red(f"{self.feature_name}: Hangup received from {addr}. Connection closed. \n")
            elif message_name == 'UNSUPPORTED_MESSAGE':
                yellow(f"{self.feature_name}: Client {addr} did not support {data['messageName']}. \n")
            else:
                unsupported_message = messenger_pb2.UnsupportedMessage()
                unsupported_message.message_name = message_name
                conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to known client {addr}. \n")

        # Unknown client handling
        else:
            # Connect new client or raise error message
            if message_name == 'CONNECT_CLIENT':
                data['conn'] = conn
                data['addr'] = addr
                data['lastActive'] = time.time()
                data['ping_sent'] = False
                self.subscriber_dict[subscriberIP] = data
                response = messenger_pb2.ConnectionResponse()
                response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
                response.udpPort = self.forwarding_port
                conn.send(serialize_msg('CONNECTION_RESPONSE', response))
                green(f"{self.feature_name}: Connected with {addr}. \n")
            else:
                unsupported_message = messenger_pb2.UnsupportedMessage()
                unsupported_message.message_name = message_name
                conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to unknown client {addr}. \n")

    def _check_clients_active(self):
        """Check if clients are still active using ping/pong"""
        if len(self.subscriber_dict) == 0:
            return
        for subscriberIP, data in list(self.subscriber_dict.items()):
            if time.time() - data['lastActive'] > self.ping_timeout and not data['ping_sent']:
                conn = data['conn']
                from utils import ping
                conn.send(serialize_msg('PING', ping))
                self.subscriber_dict[subscriberIP]['ping_sent'] = True
                yellow(f"{self.feature_name}: Client not responding. Ping sent to {data['addr']}")
            elif time.time() - data['lastActive'] > 2 * self.ping_timeout and data['ping_sent']:
                hangup = messenger_pb2.HangUp()
                hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                conn = data['conn']
                conn.send(serialize_msg('HANGUP', hangup))
                conn.close()
                red(f"{self.feature_name}: Client not responding to Ping. Connection closed to {data['addr']}. \n")
                # Also remove from connected_clients if present
                for user_id, client_info in list(self.connected_clients.items()):
                    if client_info.get('addr') == data['addr']:
                        del self.connected_clients[user_id]
                        break
                del self.subscriber_dict[subscriberIP]

    def _handle_chat_message(self, subscriberIP, addr, conn, payload):
        """Handle CHAT_MESSAGE"""
        # Update client activity
        if subscriberIP in self.subscriber_dict:
            self.subscriber_dict[subscriberIP]['lastActive'] = time.time()
            self.subscriber_dict[subscriberIP]['ping_sent'] = False

        # Register client for message delivery
        if 'author' in payload:
            user_id = payload['author'].get('userId')
            if user_id:
                self.connected_clients[user_id] = {
                    'conn': conn,
                    'addr': addr,
                    'lastActive': time.time()
                }
                print(f"[REGISTERED] Client {user_id} registered from {addr}")

        # Process the chat message
        response = self._process_chat_message_from_payload(payload, conn, addr)
        
        # Send response back to client
        if response:
            self._send_response(conn, response)

    def _process_chat_message_from_payload(self, payload, client_socket, addr):
        """Process a chat message from parsed payload"""
        print(f"[CHAT MESSAGE] from {addr}")
        print(f"  Author: {payload.get('author', {}).get('userId', 'unknown')}@{payload.get('author', {}).get('serverId', 'unknown')}")
        print(f"  Message Snowflake: {payload.get('messageSnowflake', 'unknown')}")

        # Convert payload dict back to protobuf message
        chat_msg = messenger_pb2.ChatMessage()
        
        # Reconstruct the protobuf message from the dictionary
        if 'messageSnowflake' in payload:
            chat_msg.messageSnowflake = int(payload['messageSnowflake'])
        
        if 'author' in payload:
            author_data = payload['author']
            if 'userId' in author_data:
                chat_msg.author.userId = author_data['userId']
            if 'serverId' in author_data:
                chat_msg.author.serverId = author_data['serverId']
        
        # Handle recipient
        if 'user' in payload:
            user_data = payload['user']
            if 'userId' in user_data:
                chat_msg.user.userId = user_data['userId']
            if 'serverId' in user_data:
                chat_msg.user.serverId = user_data['serverId']
        elif 'group' in payload:
            group_data = payload['group']
            if 'groupId' in group_data:
                chat_msg.group.groupId = group_data['groupId']
            if 'serverId' in group_data:
                chat_msg.group.serverId = group_data['serverId']
        
        # Handle content
        if 'textContent' in payload:
            chat_msg.textContent = payload['textContent']
        elif 'liveLocation' in payload:
            live_location_data = payload['liveLocation']
            # Reconstruct LiveLocation from dictionary
            if 'user' in live_location_data:
                user_data = live_location_data['user']
                if 'userId' in user_data:
                    chat_msg.live_location.user.userId = user_data['userId']
                if 'serverId' in user_data:
                    chat_msg.live_location.user.serverId = user_data['serverId']
            if 'timestamp' in live_location_data:
                chat_msg.live_location.timestamp = float(live_location_data['timestamp'])
            if 'expiryAt' in live_location_data:
                chat_msg.live_location.expiry_at = float(live_location_data['expiryAt'])
            if 'location' in live_location_data:
                location_data = live_location_data['location']
                if 'latitude' in location_data:
                    chat_msg.live_location.location.latitude = float(location_data['latitude'])
                if 'longitude' in location_data:
                    chat_msg.live_location.location.longitude = float(location_data['longitude'])
        
        # Use existing process_chat_message function
        return self._process_chat_message(chat_msg, client_socket, addr)

    def _process_chat_message(self, chat_msg, source_socket, source_addr):
        """
        Process incoming chat message according to the protocol:
        - Route message based on recipient type
        - Return ChatMessageResponse
        """
        author = chat_msg.author
        recipient_type = chat_msg.WhichOneof('recipient')
        content_type = chat_msg.WhichOneof('content')

        print(f"  Content type: {content_type}")
        if content_type == 'textContent':
            print(f"  Text content: {chat_msg.textContent}")
        elif content_type == 'live_location':
            print(f"  Live location from: {chat_msg.live_location.user.userId}")

        # Create response message
        response = messenger_pb2.ChatMessageResponse()
        response.messageSnowflake = chat_msg.messageSnowflake

        if recipient_type == 'user':
            target_user = chat_msg.user
            print(f"  Recipient: User {target_user.userId}@{target_user.serverId}")
            
            status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
            if target_user.serverId == self.server_id:
                # Recipient is on this server
                if target_user.userId in self.connected_clients:
                    print(f"  Action: Relay to local user {target_user.userId}")
                    self._relay_to_local_client(target_user.userId, chat_msg)
                else:
                    print(f"  User {target_user.userId} not found on this server")
                    status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
            else:
                # Recipient is on another server
                print(f"  Action: Relay to server {target_user.serverId}")
                success = self._relay_to_other_server(target_user.serverId, chat_msg)
                if not success:
                    status = messenger_pb2.ChatMessageResponse.Status.OTHER_SERVER_NOT_FOUND

            # Add delivery status
            delivery_status = response.statuses.add()
            delivery_status.user.CopyFrom(target_user)
            delivery_status.status = status

        elif recipient_type == 'group':
            target_group = chat_msg.group
            print(f"  Recipient: Group {target_group.groupId}@{target_group.serverId}")
            
            if target_group.serverId == self.server_id:
                # Group is hosted here - split into UserOfGroup messages
                print(f"  Action: Group {target_group.groupId} is local. Splitting message.")
                members = self._get_group_members(target_group.groupId, target_group.serverId)
                
                for member_user_id, member_server_id in members:
                    # Create UserOfGroup message
                    uog_msg = messenger_pb2.ChatMessage()
                    uog_msg.CopyFrom(chat_msg)
                    # Clear the group recipient and set userOfGroup
                    uog_msg.ClearField('group')
                    uog_msg.userOfGroup.user.userId = member_user_id
                    uog_msg.userOfGroup.user.serverId = member_server_id
                    uog_msg.userOfGroup.group.CopyFrom(target_group)
                    
                    print(f"    Relaying to UserOfGroup: {member_user_id}@{member_server_id}")
                    member_response = self._process_chat_message(uog_msg, None, None)
                    if member_response:
                        # Merge member responses into main response
                        for status in member_response.statuses:
                            response.statuses.append(status)
            else:
                # Group is on another server
                print(f"  Action: Relay to server {target_group.serverId}")
                success = self._relay_to_other_server(target_group.serverId, chat_msg)
                status = messenger_pb2.ChatMessageResponse.Status.DELIVERED if success else messenger_pb2.ChatMessageResponse.Status.OTHER_SERVER_NOT_FOUND
                
                # Add status for the group (represented by a placeholder user)
                delivery_status = response.statuses.add()
                delivery_status.user.userId = f"group_{target_group.groupId}"
                delivery_status.user.serverId = target_group.serverId
                delivery_status.status = status

        elif recipient_type == 'userOfGroup':
            target_uog = chat_msg.userOfGroup
            print(f"  Recipient: UserOfGroup {target_uog.user.userId}@{target_uog.user.serverId} in {target_uog.group.groupId}@{target_uog.group.serverId}")
            
            if target_uog.group.serverId == self.server_id:
                # User is part of a group hosted on this server
                if target_uog.user.userId in self.connected_clients:
                    print(f"  Action: Relay to local user {target_uog.user.userId}")
                    self._relay_to_local_client(target_uog.user.userId, chat_msg)
                    status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
                else:
                    print(f"  User {target_uog.user.userId} not found")
                    status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
                    
                delivery_status = response.statuses.add()
                delivery_status.user.CopyFrom(target_uog.user)
                delivery_status.status = status
            else:
                # UserOfGroup for a group on another server - this is an error
                print(f"  Error: UserOfGroup for group on another server {target_uog.group.serverId}")
                delivery_status = response.statuses.add()
                delivery_status.user.CopyFrom(target_uog.user)
                delivery_status.status = messenger_pb2.ChatMessageResponse.Status.OTHER_ERROR

        else:
            print(f"  Unknown recipient type: {recipient_type}")
            # Add error status
            delivery_status = response.statuses.add()
            delivery_status.user.CopyFrom(author)  # Return error to sender
            delivery_status.status = messenger_pb2.ChatMessageResponse.Status.OTHER_ERROR

        return response

    def _relay_to_local_client(self, user_id, chat_msg):
        """Relay message to a local client using standard format"""
        if user_id in self.connected_clients:
            try:
                client_info = self.connected_clients[user_id]
                conn = client_info['conn']
                # Use standard format for sending
                msg = serialize_msg('CHAT_MESSAGE', chat_msg)
                conn.send(msg)
                print(f"    Successfully relayed to local client {user_id}")
                return True
            except Exception as e:
                print(f"    Error relaying to local client {user_id}: {e}")
                # Remove disconnected client
                del self.connected_clients[user_id]
                return False
        else:
            print(f"    Client {user_id} not connected")
            return False

    def _relay_to_other_server(self, server_id, chat_msg):
        """Relay message to another server"""
        if server_id in self.server_directory:
            try:
                host, port = self.server_directory[server_id]
                print(f"    Relaying to server {server_id} at {host}:{port}")
                
                # Create a connection to the other server
                other_server_conn = ConnectionHandler()
                other_server_conn.start_client(host, port)
                
                # Send the chat message using standard format
                msg = serialize_msg('CHAT_MESSAGE', chat_msg)
                other_server_conn.send_msg(msg)
                
                # Wait for response from the other server
                try:
                    response_msg, response_addr, response_conn = other_server_conn.recv_msg()
                    response_name, response_size, response_payload = parse_msg(response_msg)
                    
                    if response_name == 'CHAT_MESSAGE_RESPONSE':
                        print(f"    Received response from server {server_id}")
                        # Could process the response here if needed
                    else:
                        print(f"    Unexpected response from server {server_id}: {response_name}")
                        
                except Exception as e:
                    print(f"    No response received from server {server_id}: {e}")
                
                # Close the connection
                other_server_conn.close()
                print(f"    Successfully relayed message to server {server_id}")
                return True
                
            except ConnectionRefusedError:
                print(f"    Connection refused by server {server_id} at {host}:{port}")
                return False
            except Exception as e:
                print(f"    Error relaying to server {server_id}: {e}")
                return False
        else:
            print(f"    Server {server_id} not found in directory")
            return False

    def _get_group_members(self, group_id, group_server_id):
        """Get members of a group"""
        group_key = (group_id, group_server_id)
        if group_key in self.group_members:
            return self.group_members[group_key]
        else:
            # Return some example members for testing
            print(f"    Group {group_id} not found, returning example members")
            return [("user1", self.server_id), ("user2", self.server_id)]

    def _send_response(self, conn, response):
        """Send ChatMessageResponse back to client using standard format"""
        try:
            # Use standard format for sending response
            msg = serialize_msg('CHAT_MESSAGE_RESPONSE', response)
            conn.send(msg)
            print(f"  Sent response with {len(response.statuses)} delivery statuses")
        except Exception as e:
            print(f"  Error sending response: {e}")

    def register_server(self, server_id, host, port):
        """Register a new server in the directory for inter-server communication"""
        self.server_directory[server_id] = (host, port)
        print(f"[SERVER REGISTRY] Registered server {server_id} at {host}:{port}")

    def unregister_server(self, server_id):
        """Remove a server from the directory"""
        if server_id in self.server_directory:
            del self.server_directory[server_id]
            print(f"[SERVER REGISTRY] Unregistered server {server_id}")
            return True
        return False

# Global chat service instance
chat_service = None

def start_server():
    """Start the chat server using ServiceBase pattern"""
    global chat_service
    print(f"[STARTING] Chat server on {HOST}:{PORT} with SERVER_ID: {SERVER_ID}")
    
    try:
        chat_service = ChatService()
        chat_service.handle_connections()
    except KeyboardInterrupt:
        print("[SHUTTING DOWN] Chat server is shutting down.")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")

if __name__ == '__main__':
    start_server()
