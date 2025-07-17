import queue
import time

from utils import ConnectionHandler, red, yellow, green, blue, parse_msg, serialize_msg, connect_client, ping, pong
from typing import Literal
from config import config

from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES', 'TRANSLATION', 'documents']

class FeatureBase:
    """
    Base class for handling feature-specific client connections.

    Attributes:
        feature_name (FeatureName): The name of the feature this instance represents.

    Methods:
        handle_connection(server_list):
            Handles the process of connecting to the appropriate server for the feature.
            - Looks up the server and port for the feature in the provided server list.
            - Establishes a client connection using ConnectionHandler.
            - Sends a connection request and processes the server's response.
            - Handles connection errors and prints status messages.
    """
    def __init__(self, feature_name: FeatureName):
        self.feature_name = feature_name
        self._running = True
        self.udp_server_port = None
        self.server_address = None
        self.client = None  # Initialize client as None

        # Check: server still active?
        self.last_msg_received_time = None
        self.ping_sent = False
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def is_connected(self):
        """Check if the client is connected to the server."""
        return self._running and self.client is not None

    def handle_connection(self, server_list):

        try:
            self.feature_ip, self.feature_port, self.udp_server_port = self._get_server_for_feature(server_list)
        except ValueError as e:
            red(str(e))
            return
        
        self.server_address = self.feature_ip

        if self.feature_ip is None or self.feature_port is None:
            return

        try:
            self.client = ConnectionHandler(timeout=self.ping_timeout)
            self.client.start_client(self.feature_ip, self.feature_port)

            self._send_connection_request()
            while self._running:
                # Check: server still active?
                try:
                    msg, addr, _ = self.client.recv_msg()
                    message_name, _, payload = parse_msg(msg)
                    self.last_msg_received_time = time.time()
                    self.ping_sent = False
                except queue.Empty:
                    # only send ping if no TCP and UDP message is in the queue
                    if self.ping_sent:
                        hangup = messenger_pb2.HangUp()
                        hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                        self.client.send_msg(serialize_msg('HANGUP', hangup))
                        self.client.close()
                        self._running = False
                        red(f"Server not active anymore. {self.feature_name} connection closed to {self.feature_ip}:{self.feature_port} \n")
                        break
                    elif time.time() - self.last_msg_received_time > self.ping_timeout:
                        self.client.send_msg(serialize_msg('PING', ping))
                        self.ping_sent = True
                        yellow(f"Server not responding. Ping sent for {self.feature_name} to {self.feature_ip}:{self.feature_port}. \n")
                        continue
                    else:
                        continue

                    # Handle messages; pass client conn and address
                print(f"Received message '{message_name}' from {addr} for {self.feature_name} on {self.feature_ip}:{self.feature_port} - {payload}")
                message_handled = self.handle_message_for_feature(message_name, payload, self.client, addr)
                if not message_handled:
                    self._handle_base_messages(message_name, payload, self.client, addr)

        except Exception as e:
            red(f"Failed to connect to {self.feature_name} on {self.feature_ip}:{self.feature_port}. Error: {e} \n")
            self.client.close()
            self._running = False
    
    def _send_connection_request(self):
        if self.feature_name == 'TYPING_INDICATOR':
            connect_client.udpPort = config['typing_feature']['client_udp_port']
        elif self.feature_name == 'LIVE_LOCATION':
            connect_client.udpPort = config['location_feature']['client_udp_port']
        elif self.feature_name == 'MESSAGES':
            connect_client.udpPort = 0  # Chat uses TCP only, no UDP needed
        elif self.feature_name == 'TRANSLATION':
            connect_client.udpPort = 0  # Translation uses TCP only, no UDP needed
        elif self.feature_name == 'DOCUMENT':
            connect_client.udpPort = 0  # Document uses TCP only, no UDP needed

        self.client.send_msg(serialize_msg('CONNECT_CLIENT', connect_client))
        blue(f"Trying to connect to feature: '{self.feature_name}'...")

    def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
        """
        Updated for each feature individually if it receives messages beyond the _handle_base_messages function
        """
        return False

    def _handle_base_messages(self, message_name=None, payload=None, conn=None, addr=None):
        # Handle connection response
        if message_name == 'CONNECTED':
            if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                yellow(f"Already subscribed to {self.feature_name} on {self.feature_ip}:{self.feature_port} \n")
            elif payload['result'] == 'CONNECTED':
                green(f"CONNECTED to {self.feature_name} on {self.feature_ip}:{self.feature_port} \n")
            else:
                red(f"Unknown connection response for {self.feature_name} from {self.feature_ip}:{self.feature_port}. Check the payload of the connection response. \n")

        # Handle Ping-Pong
        elif message_name == 'PING':
            print(f"Received PING for {self.feature_name} from {self.feature_ip}:{self.feature_port}")
            self.client.send_msg(serialize_msg('PONG', pong))
            green(f"Responded with PONG for {self.feature_name} to {self.feature_ip}:{self.feature_port} \n")
        elif message_name == 'PONG':
            green(f"Pong received for {self.feature_name} from {self.feature_ip}:{self.feature_port} \n")

        # Handle Hangup
        elif message_name == 'HANGUP':
            self.client.close()
            self._running = False
            red(f"Server closes. {self.feature_name} connection closed to {self.feature_ip}:{self.feature_port}. \n")

        # Handle Receive Unsupported Message
        elif message_name == 'UNSUPPORTED_MESSAGE':
            yellow(f"Server {self.feature_ip}:{self.feature_port} does not support {payload['messageName']}. \n")

        # Handle all other (unsupported) messages
        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            self.client.send_msg(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"Unsupported message '{message_name}' received. Notified server at {self.feature_ip}:{self.feature_port}. \n")

    def _get_server_for_feature(self, server_list):
        for feature_server in server_list:
            for features in feature_server['feature']:
                if features['featureName'] == self.feature_name:
                    # For MESSAGES feature, only connect to the server specified in config
                    if self.feature_name == 'MESSAGES':
                        if feature_server.get('serverId') == config['user']['serverId']:
                            return feature_server['server_ip'], features['port'], features.get('udpPort')
                    else:
                        return feature_server['server_ip'], features['port'], features.get('udpPort')

        raise ValueError(f"Could not connect to feature '{self.feature_name}'. Not found in provided server list.")

    def stop(self):
        """Gracefully stop the feature process when client UI is closed."""

        self._running = False
        if self.client is not None:
            try:
                hangup = messenger_pb2.HangUp()
                hangup.reason = messenger_pb2.HangUp.Reason.EXIT
                self.client.send_msg(serialize_msg('HANGUP', hangup))
                self.client.close()
                red(f"{self.feature_name}: Client is closing. Connection is closed and the server notified. \n")
            except Exception as e:
                red(f"{self.feature_name}: Unknown error while closing client: {e}")
        else:
            red(f"{self.feature_name}: Client already closed.\n")
