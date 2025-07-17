import queue
import time
import threading
from typing import Literal
from utils import ConnectionHandler, parse_msg, serialize_msg, red, green, yellow, blue, ping, pong, connect_server
from config import config
from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES']

class ServiceBase:
    def __init__(self, feature_name : FeatureName, bind_port, forwarding_port=None):
        self.feature_name = feature_name

        self.server = None
        self._running = True
        self.subscriber_dict = {}   # dict to store feature subscribers
        self.connected_servers = {}  # dict to store server-to-server connections {server_id: {conn, features, addr, lastActive}}
        self.bind_ip = config['address']
        self.bind_port = bind_port
        self.forwarding_port = forwarding_port

        # Check: client still active?
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def set_server_list_and_connect(self, server_list):
        """Set server list and connect to other servers (similar to client pattern)"""
        if not server_list:
            return
            
        blue(f"{self.feature_name}: Connecting to {len(server_list)} discovered servers...")
        for server_info in server_list:
            # Skip our own server
            if server_info.get('serverId') == config.get('serverId'):
                continue
                
            # Find port for this feature
            server_port = None
            for feature in server_info.get('feature', []):
                if feature.get('featureName') == self.feature_name:
                    server_port = feature.get('port')
                    break
            
            if server_port:
                # Start connection in separate thread (similar to client)
                threading.Thread(
                    target=self._handle_server_connection,
                    args=(server_info['server_ip'], server_port, server_info.get('serverId')),
                    daemon=True
                ).start()

    def _handle_server_connection(self, server_ip, server_port, server_id):
        """Handle connection to another server (similar to client FeatureBase.handle_connection)"""
        try:
            client = ConnectionHandler(timeout=self.ping_timeout)
            client.start_client(server_ip, server_port)

            # Send CONNECT_SERVER request (similar to client CONNECT_CLIENT)
            connect_server.serverId = config['serverId']
            connect_server.features[:] = [self.feature_name]  # Offer this feature
            client.send_msg(serialize_msg('CONNECT_SERVER', connect_server))
            blue(f"{self.feature_name}: Trying to connect to server '{server_id}' at {server_ip}:{server_port}...")

            # Store connection info
            self.connected_servers[server_id] = {
                'conn': client,
                'addr': (server_ip, server_port),
                'lastActive': time.time(),
                'ping_sent': False,
                'features': []
            }

            # Message handling loop (similar to client)
            while self._running and server_id in self.connected_servers:
                try:
                    msg, addr, _ = client.recv_msg()
                    message_name, _, payload = parse_msg(msg)
                    self.connected_servers[server_id]['lastActive'] = time.time()
                    self.connected_servers[server_id]['ping_sent'] = False
                except queue.Empty:
                    # Handle ping/timeout (similar to client logic)
                    server_info = self.connected_servers.get(server_id)
                    if not server_info:
                        break
                        
                    if server_info['ping_sent']:
                        hangup = messenger_pb2.HangUp()
                        hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                        client.send_msg(serialize_msg('HANGUP', hangup))
                        client.close()
                        del self.connected_servers[server_id]
                        red(f"{self.feature_name}: Server {server_id} not active anymore. Connection closed to {server_ip}:{server_port}")
                        break
                    elif time.time() - server_info['lastActive'] > self.ping_timeout:
                        client.send_msg(serialize_msg('PING', ping))
                        self.connected_servers[server_id]['ping_sent'] = True
                        yellow(f"{self.feature_name}: Server {server_id} not responding. Ping sent to {server_ip}:{server_port}")
                        continue
                    else:
                        continue

                print(f"{self.feature_name}: Received server message '{message_name}' from {server_id} at {server_ip}:{server_port} - {payload}")
                
                # Handle server messages (similar to client base messages)
                message_handled = self.handle_server_message_for_feature(message_name, payload, client, addr, server_id)
                if not message_handled:
                    self._handle_base_server_messages(message_name, payload, client, addr, server_id)

        except Exception as e:
            red(f"{self.feature_name}: Failed to connect to server {server_id} on {server_ip}:{server_port}. Error: {e}")
            if server_id in self.connected_servers:
                self.connected_servers[server_id]['conn'].close()
                del self.connected_servers[server_id]

    def handle_server_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None, server_id=None):
        """Override this method in subclasses to handle server-specific messages"""
        return False

    def _handle_base_server_messages(self, message_name=None, payload=None, conn=None, addr=None, server_id=None):
        """Handle base server messages (similar to client _handle_base_messages)"""
        if message_name == 'CONNECTED':
            if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                yellow(f"{self.feature_name}: Already connected to server {server_id}")
            elif payload['result'] == 'CONNECTED':
                green(f"{self.feature_name}: CONNECTED to server {server_id}")
            else:
                red(f"{self.feature_name}: Unknown connection response from server {server_id}")

        elif message_name == 'PING':
            conn.send_msg(serialize_msg('PONG', pong))
            green(f"{self.feature_name}: Responded with PONG to server {server_id}")
        elif message_name == 'PONG':
            green(f"{self.feature_name}: Pong received from server {server_id}")

        elif message_name == 'HANGUP':
            conn.close()
            if server_id in self.connected_servers:
                del self.connected_servers[server_id]
            red(f"{self.feature_name}: Server {server_id} closed connection")

        elif message_name == 'UNSUPPORTED_MESSAGE':
            yellow(f"{self.feature_name}: Server {server_id} does not support {payload['messageName']}")

        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            conn.send_msg(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"{self.feature_name}: Unsupported message '{message_name}' received from server {server_id}")

    def broadcast_to_servers(self, message_name, payload):
        """Broadcast message to all connected servers"""
        for server_id, server_info in self.connected_servers.items():
            try:
                server_info['conn'].send_msg(serialize_msg(message_name, payload))
                blue(f"{self.feature_name}: Sent {message_name} to server {server_id}")
            except Exception as e:
                red(f"{self.feature_name}: Failed to send {message_name} to server {server_id}: {e}")

    def handle_connections(self):
        self.server = ConnectionHandler(timeout=self.ping_timeout)
        self.server.start_server(self.bind_ip, self.bind_port)

        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while self._running:
            # Check: client and server still active
            def are_peers_active():
                # Check clients
                if len(self.subscriber_dict) > 0:
                    for addr, data in list(self.subscriber_dict.items()):
                        if time.time() - data['lastActive'] > self.ping_timeout and not data['ping_sent']:
                            conn = data['conn']
                            conn.send(serialize_msg('PING', ping))
                            self.subscriber_dict[addr]['ping_sent'] = True
                            yellow(f"{self.feature_name}: Client not responding. Ping sent to {data['addr']}")
                        elif time.time() - data['lastActive'] > 2 * self.ping_timeout and data['ping_sent']:
                            hangup = messenger_pb2.HangUp()
                            hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                            conn = data['conn']
                            conn.send(serialize_msg('HANGUP', hangup))
                            conn.close()
                            red(f"{self.feature_name}: Client not responding to Ping. Connection closed to {data['addr']}. \n")
                            del self.subscriber_dict[addr]
                
                # Check servers
                if len(self.connected_servers) > 0:
                    for server_id, server_data in list(self.connected_servers.items()):
                        if time.time() - server_data['lastActive'] > self.ping_timeout and not server_data['ping_sent']:
                            conn = server_data['conn']
                            conn.send(serialize_msg('PING', ping))
                            self.connected_servers[server_id]['ping_sent'] = True
                            yellow(f"{self.feature_name}: Server {server_id} not responding. Ping sent to {server_data['addr']}")
                        elif time.time() - server_data['lastActive'] > 2 * self.ping_timeout and server_data['ping_sent']:
                            hangup = messenger_pb2.HangUp()
                            hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                            conn = server_data['conn']
                            conn.send(serialize_msg('HANGUP', hangup))
                            conn.close()
                            red(f"{self.feature_name}: Server {server_id} not responding to Ping. Connection closed to {server_data['addr']}. \n")
                            del self.connected_servers[server_id]

            try:
                msg, addr, conn = self.server.recv_msg()

                message_name, _, data = parse_msg(msg)
            except queue.Empty:
                are_peers_active()
                continue
            are_peers_active()

            # Known client/server handling
            if addr in self.subscriber_dict.keys():
                # Client handling - update data
                self.subscriber_dict[addr]['lastActive'] = time.time()
                self.subscriber_dict[addr]['ping_sent'] = False
                # Handle messages
                message_handled = self.handle_message_for_feature(message_name, data, conn, addr)
                if not message_handled:
                    self._handle_base_messages(message_name, data, conn, addr)
            
            # Check if it's a known server connection
            elif any(server_info['addr'] == addr for server_info in self.connected_servers.values()):
                # Server handling - find the server and update data
                for server_id, server_info in self.connected_servers.items():
                    if server_info['addr'] == addr:
                        server_info['lastActive'] = time.time()
                        server_info['ping_sent'] = False
                        # Handle messages
                        message_handled = self.handle_message_for_feature(message_name, data, conn, addr)
                        if not message_handled:
                            self._handle_base_messages(message_name, data, conn, addr)
                        break

            # Unknown client/server handling
            else:
                # Connect new client or server, or raise error message
                if message_name == 'CONNECT_CLIENT':
                    data['conn'] = conn
                    data['addr'] = addr
                    data['lastActive'] = time.time()
                    data['ping_sent'] = False
                    self.subscriber_dict[addr] = data
                    response = messenger_pb2.ConnectResponse()
                    response.result = messenger_pb2.ConnectResponse.Result.CONNECTED
                    conn.send(serialize_msg('CONNECTED', response))
                    green(f"{self.feature_name}: Connected with client {data}. \n")
                    
                elif message_name == 'CONNECT_SERVER':
                    # Handle server-to-server connection
                    server_id = data.get('serverId')
                    server_features = data.get('features', [])
                    
                    if server_id in self.connected_servers:
                        # Server already connected
                        response = messenger_pb2.ConnectResponse()
                        response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
                        conn.send(serialize_msg('CONNECTED', response))
                        yellow(f"{self.feature_name}: Server {server_id} already connected. \n")
                    else:
                        # New server connection
                        self.connected_servers[server_id] = {
                            'conn': conn,
                            'addr': addr,
                            'features': server_features,
                            'lastActive': time.time(),
                            'ping_sent': False
                        }
                        response = messenger_pb2.ConnectResponse()
                        response.result = messenger_pb2.ConnectResponse.Result.CONNECTED
                        conn.send(serialize_msg('CONNECTED', response))
                        green(f"{self.feature_name}: Connected with server {server_id} offering features {server_features}. \n")
                else:
                    unsupported_message = messenger_pb2.UnsupportedMessage()
                    unsupported_message.message_name = message_name
                    conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                    yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to unknown client/server {addr}. \n")


    def handle_message_for_feature(self, message_name=None, data=None, conn=None, addr=None):
        """
        Updated for each feature individually if it receives messages beyond the _handle_base_messages function
        """
        return False

    def _handle_base_messages(self, message_name=None, data=None, conn=None, addr=None):
        # Handle connection response
        if message_name == 'CONNECT_CLIENT':
            response = messenger_pb2.ConnectResponse()
            response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
            conn.send(serialize_msg('CONNECTED', response))
            yellow(f"{self.feature_name}: Client {addr} already subscribed. \n")
            
        elif message_name == 'CONNECT_SERVER':
            response = messenger_pb2.ConnectResponse()
            response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
            conn.send(serialize_msg('CONNECTED', response))
            yellow(f"{self.feature_name}: Server already connected from {addr}. \n")
        
        # Handle Ping-Pong
        elif message_name == 'PING':
            conn.send(serialize_msg('PONG', pong))
            green(f"{self.feature_name}: Pong answered to {addr}. \n")
        elif message_name == 'PONG':
            green(f"{self.feature_name}: Pong received from {addr} \n")
        
        # Handle Hangup
        elif message_name == 'HANGUP':
            # Check if it's a client or server disconnecting
            if addr in self.subscriber_dict:
                del self.subscriber_dict[addr]
                red(f"{self.feature_name}: Client hangup received from {addr}. Connection closed. \n")
            else:
                # Find and remove server connection
                for server_id, server_info in list(self.connected_servers.items()):
                    if server_info['addr'] == addr:
                        del self.connected_servers[server_id]
                        red(f"{self.feature_name}: Server {server_id} hangup received from {addr}. Connection closed. \n")
                        break
            conn.close()
        
        # Handle Receive Unsupported Message
        elif message_name == 'UNSUPPORTED_MESSAGE':
            yellow(f"{self.feature_name}: Peer {addr} did not support {data['messageName']}. \n")
        
        # Handle all other (unsupported) messages
        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to known peer {addr}. \n")

            
    def stop(self):
        """Gracefully stop the feature process when server is closing."""
        self._running = False

        # Close client connections
        client_list_text = ""
        for addr, data in list(self.subscriber_dict.items()):
            hangup = messenger_pb2.HangUp()
            hangup.reason = messenger_pb2.HangUp.Reason.EXIT
            conn = data['conn']
            conn.send(serialize_msg('HANGUP', hangup))
            conn.close()
            client_list_text += f" {data['addr']}"
        if client_list_text:
            red(f"{self.feature_name}: Server is closing. Client connections closed to{client_list_text}. \n")

        # Close server connections
        server_list_text = ""
        for server_id, server_data in list(self.connected_servers.items()):
            hangup = messenger_pb2.HangUp()
            hangup.reason = messenger_pb2.HangUp.Reason.EXIT
            conn = server_data['conn']
            conn.send(serialize_msg('HANGUP', hangup))
            conn.close()
            server_list_text += f" {server_id}"
        if server_list_text:
            red(f"{self.feature_name}: Server is closing. Server connections closed to{server_list_text}. \n")

        self.server.close()
