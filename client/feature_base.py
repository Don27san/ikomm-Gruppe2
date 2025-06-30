import queue
import time

from utils import ConnectionHandler, red, yellow, green, blue, parse_msg, serialize_msg, connect_client, ping, pong
from typing import Literal
from config import config

from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT_MESSAGE']

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

        # Check: server still active?
        self.last_msg_received_time = None
        self.ping_sent = False
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def handle_connection(self, server_list):

        feature_ip, feature_port = self._get_server_for_feature(server_list)

        if feature_ip is None or feature_port is None:
            return

        try:
            client = ConnectionHandler(timeout=self.ping_timeout)
            client.start_client(feature_ip, feature_port)

            client.send_msg(serialize_msg('CONNECT_CLIENT', connect_client))
            blue(f'Trying to connect to feature: {self.feature_name}...')
            while self._running:
                # Check: server still active?
                try:
                    msg, addr, _ = client.recv_msg()
                    message_name, _, payload = parse_msg(msg)
                    self.last_msg_received_time = time.time()
                    self.ping_sent = False
                except queue.Empty:
                    # only send ping if no TCP and UDP message is received
                    if self.ping_sent:
                        hangup = messenger_pb2.HangUp()
                        hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                        client.send_msg(serialize_msg('HANGUP', hangup))
                        client.close()
                        self._running = False
                        red(f"Server not active anymore. {self.feature_name} connection closed to {feature_ip}:{feature_port} \n")
                        break
                    elif time.time() - self.last_msg_received_time > self.ping_timeout:
                        client.send_msg(serialize_msg('PING', ping))
                        self.ping_sent = True
                        yellow(f"Server not responding. Ping sent for {self.feature_name} to {feature_ip}:{feature_port}. \n")
                        continue
                    else:
                        continue

                if message_name == 'CONNECTION_RESPONSE':
                    if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                        yellow(f"Already connected to {self.feature_name} on {feature_ip}:{feature_port} \n")
                    elif payload['result'] == 'CONNECTED':
                        green(f"Connected to {self.feature_name} on {feature_ip}:{feature_port} \n")
                    else:
                        red(f"Unknown connection response for {self.feature_name} from {feature_ip}:{feature_port} \n")
                    if 'udpPort' in payload:
                        self.server_address = addr[0]
                        self.udp_server_port = payload['udpPort']
                elif message_name == 'PONG':
                    green(f"Pong received for {self.feature_name} from {feature_ip}:{feature_port} \n")
                elif message_name == 'PING':
                    client.send_msg(serialize_msg('PONG', pong))
                    green(f"Answered PONG for {self.feature_name} to {feature_ip}:{feature_port} \n")
                elif message_name == 'HANGUP':
                    client.close()
                    self._running = False
                    red(f"Server closes. {self.feature_name} connection closed to {feature_ip}:{feature_port}. \n")
                elif message_name == 'UNSUPPORTED_MESSAGE':
                    yellow(f"Server {feature_ip}:{feature_port} does not support {payload['messageName']}. \n")
                else:
                    unsupported_message = messenger_pb2.UnsupportedMessage()
                    unsupported_message.message_name = message_name
                    client.send_msg(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                    yellow(f"Received {message_name} is not supported. Error message sent to {feature_ip}:{feature_port}. \n")

        except Exception as e:
            red(f"Failed to connect to {self.feature_name} on {feature_ip}:{feature_port}. Error: {e} \n")
            client.close()
            self._running = False

    def _get_server_for_feature(self, server_list):
        for feature_server in server_list:
            for features in feature_server['feature']:
                if features['featureName'] == self.feature_name:
                    return feature_server['server_ip'], features['port']

        red(f'Could not find server in server_list: {server_list} hosting feature {self.feature_name}')
        return None, None