from utils import ConnectionHandler, red, yellow, green, blue, parse_msg, serialize_msg, connect_client
from typing import Literal

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

    def handle_connection(self, server_list):

        feature_ip, feature_port = self._get_server_for_feature(server_list)

        if feature_ip is None or feature_port is None:
            return

        try:
            client = ConnectionHandler()
            client.start_client(feature_ip, feature_port)

            client.send_msg(serialize_msg('CONNECT_CLIENT', connect_client))
            blue(f'Trying to connect to feature: {self.feature_name}...')
            while True:
                msg = client.recv_msg()[0]
                message_name, _, payload = parse_msg(msg)

                if message_name == 'CONNECTION_RESPONSE':
                    if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                        yellow(f"Already connected to {self.feature_name} on {feature_ip}:{feature_port} \n")
                    elif payload['result'] == 'CONNECTED':
                        green(f"Connected to {self.feature_name} on {feature_ip}:{feature_port} \n")
                    else:
                        red(f"Unknown connection response for {self.feature_name} from {feature_ip}:{feature_port} \n")

        except Exception as e:
            red(f"Failed to connect to {self.feature_name} on {feature_ip}:{feature_port}. Error: {e} \n")
            client.close()

    def _get_server_for_feature(self, server_list):
        for feature_server in server_list:
            for features in feature_server['feature']:
                if features['featureName'] == self.feature_name:
                    return feature_server['server_ip'], features['port']

        red(f'Could not find server in server_list: {server_list} hosting feature {self.feature_name}')
        return None, None