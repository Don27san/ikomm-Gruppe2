import queue
import time
import threading

from utils import ConnectionHandler, red, yellow, green, blue, parse_msg, serialize_msg, connect_server, ping, pong
from typing import Literal
from config import config

from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES', 'TRANSLATION', 'DOCUMENT']

class ServerConnectionBase:
    """
    Base class for handling server-to-server connections.

    Attributes:
        offered_features (list): List of features this server offers to other servers.

    Methods:
        handle_server_connections(server_list):
            Handles the process of connecting to other servers for inter-server communication.
            - Looks up servers and their features in the provided server list.
            - Establishes server connections using ConnectionHandler.
            - Sends connection requests and processes server responses.
            - Handles connection errors and prints status messages.
    """
    def __init__(self, offered_features: list[FeatureName]):
        self.offered_features = offered_features
        self._running = True
        self.connected_servers = {}  # Dict to store server connections {server_id: {conn, features, addr, lastActive}}

        # Check: server still active?
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def is_connected_to_server(self, server_id):
        """Check if connected to a specific server."""
        return server_id in self.connected_servers and self.connected_servers[server_id]['conn'] is not None

    def handle_server_connections(self, server_list):
        """Connect to all discovered servers."""
        for server_info in server_list:
            server_id = server_info.get('serverId')
            server_ip = server_info.get('server_ip')
            
            if not server_id or not server_ip:
                continue
                
            # Find a suitable feature port to connect to
            connection_port = self._find_connection_port(server_info)
            if connection_port:
                # Start connection in separate thread
                threading.Thread(target=self._connect_to_server, 
                               args=(server_id, server_ip, connection_port), 
                               daemon=True).start()
            else:
                yellow(f"No suitable connection port found for server {server_id}")

    def _find_connection_port(self, server_info):
        """Find a suitable port to connect to the server."""
        features = server_info.get('feature', [])
        # Try to find a feature we support for connection
        for feature in features:
            feature_name = feature.get('featureName')
            if feature_name in self.offered_features:
                return feature.get('port')
        
        # If no common features, try the first available feature
        if features:
            return features[0].get('port')
        
        return None

    def _connect_to_server(self, server_id, server_ip, server_port):
        """Establish connection to a specific server."""
        try:
            client = ConnectionHandler(timeout=self.ping_timeout)
            client.start_client(server_ip, server_port)

            # Send connection request
            connect_server_msg = messenger_pb2.ConnectServer()
            connect_server_msg.serverId = config['serverId']
            connect_server_msg.features.extend(self.offered_features)
            print("self.offeredfeature: ", self.offered_features)
            
            client.send_msg(serialize_msg('CONNECT_SERVER', connect_server_msg))
            blue(f"Connecting to server '{server_id}' at {server_ip}:{server_port}...")

            # Store connection info
            self.connected_servers[server_id] = {
                'conn': client,
                'addr': f"{server_ip}:{server_port}",
                'features': self.offered_features.copy(),
                'lastActive': time.time(),
                'ping_sent': False
            }

            # Start handling messages for this server connection
            self._handle_server_messages(server_id, client)

        except Exception as e:
            red(f"Failed to connect to server {server_id} at {server_ip}:{server_port}. Error: {e}")

    def _handle_server_messages(self, server_id, client):
        """Handle incoming messages from a connected server."""
        while self._running and server_id in self.connected_servers:
            try:
                msg, addr, _ = client.recv_msg()
                message_name, _, payload = parse_msg(msg)
                
                # Update last active time
                self.connected_servers[server_id]['lastActive'] = time.time()
                self.connected_servers[server_id]['ping_sent'] = False
                
                print(f"Received message '{message_name}' from server {server_id} - {payload}")
                
                # Handle server-specific messages
                message_handled = self.handle_message_for_server(message_name, payload, client, server_id)
                if not message_handled:
                    self._handle_base_server_messages(message_name, payload, client, server_id)

            except queue.Empty:
                # Check if server is still active
                self._check_server_health(server_id)
                continue
            except Exception as e:
                red(f"Error handling messages from server {server_id}: {e}")
                self._disconnect_server(server_id)
                break

    def _check_server_health(self, server_id):
        """Check if a server is still responsive."""
        if server_id not in self.connected_servers:
            return
            
        server_info = self.connected_servers[server_id]
        current_time = time.time()
        
        if current_time - server_info['lastActive'] > self.ping_timeout and not server_info['ping_sent']:
            # Send ping
            client = server_info['conn']
            client.send_msg(serialize_msg('PING', ping))
            self.connected_servers[server_id]['ping_sent'] = True
            yellow(f"Server {server_id} not responding. Ping sent.")
        elif current_time - server_info['lastActive'] > 2 * self.ping_timeout and server_info['ping_sent']:
            # Server timeout
            hangup = messenger_pb2.HangUp()
            hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
            client = server_info['conn']
            client.send_msg(serialize_msg('HANGUP', hangup))
            red(f"Server {server_id} timeout. Disconnecting.")
            self._disconnect_server(server_id)

    def _disconnect_server(self, server_id):
        """Disconnect from a server."""
        if server_id in self.connected_servers:
            client = self.connected_servers[server_id]['conn']
            client.close()
            del self.connected_servers[server_id]
            red(f"Disconnected from server {server_id}")

    def handle_message_for_server(self, message_name=None, payload=None, conn=None, server_id=None):
        """
        Override this method in subclasses to handle server-specific messages.
        Return True if message was handled, False otherwise.
        """
        return False

    def _handle_base_server_messages(self, message_name=None, payload=None, conn=None, server_id=None):
        """Handle base server-to-server messages."""
        # Handle connection response
        if message_name == 'CONNECTED':
            if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                yellow(f"Already connected to server {server_id}")
            elif payload['result'] == 'CONNECTED':
                green(f"CONNECTED to server {server_id}")
            else:
                red(f"Unknown connection response from server {server_id}. Check the payload.")

        # Handle Ping-Pong
        elif message_name == 'PING':
            print(f"Received PING from server {server_id}")
            conn.send_msg(serialize_msg('PONG', pong))
            green(f"Responded with PONG to server {server_id}")
        elif message_name == 'PONG':
            green(f"Pong received from server {server_id}")

        # Handle Hangup
        elif message_name == 'HANGUP':
            red(f"Server {server_id} initiated hangup. Reason: {payload.get('reason', 'Unknown')}")
            self._disconnect_server(server_id)

        # Handle Receive Unsupported Message
        elif message_name == 'UNSUPPORTED_MESSAGE':
            yellow(f"Server {server_id} does not support {payload['messageName']}")

        # Handle all other (unsupported) messages
        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            conn.send_msg(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"Unsupported message '{message_name}' received from server {server_id}. Notified server.")

    def stop(self):
        """Gracefully stop all server connections."""
        self._running = False
        
        for server_id in list(self.connected_servers.keys()):
            try:
                hangup = messenger_pb2.HangUp()
                hangup.reason = messenger_pb2.HangUp.Reason.EXIT
                client = self.connected_servers[server_id]['conn']
                client.send_msg(serialize_msg('HANGUP', hangup))
                client.close()
                red(f"Server connection to {server_id} closed.")
            except Exception as e:
                red(f"Error closing connection to server {server_id}: {e}")
        
        self.connected_servers.clear()

    def broadcast_to_servers(self, message_name, payload, feature_filter=None):
        """
        Broadcast a message to all connected servers or servers supporting specific features.
        
        Args:
            message_name: The message type to send
            payload: The message payload
            feature_filter: Optional list of features - only send to servers supporting these features
        """
        for server_id, server_info in self.connected_servers.items():
            try:
                # Check if server supports required features
                if feature_filter:
                    if not any(feature in server_info['features'] for feature in feature_filter):
                        continue
                
                client = server_info['conn']
                client.send_msg(serialize_msg(message_name, payload))
                blue(f"Sent {message_name} to server {server_id}")
            except Exception as e:
                red(f"Failed to send {message_name} to server {server_id}: {e}")
