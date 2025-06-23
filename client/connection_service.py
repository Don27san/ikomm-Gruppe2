import socket
from utils import connect_client, blue, green, red, yellow, serialize_msg, parse_msg
from protobuf import messenger_pb2

class ConnectionService:
    """
    Handles discovery and connection to feature-specific servers.
    Manages sockets for each supported feature and provides a generic send() method.
    """

    def __init__(self, feature_support_list=[], server_list=[]):
        self.feature_support_list = feature_support_list
        self.server_list = server_list
        self.feature_sockets = {}  # key: feature_name, value: connected socket

    def connect_client(self):
        blue(' Connecting client to supported features ...')

        for feature_name in self.feature_support_list:
            for feature_server in self.server_list:
                for features in feature_server['feature']:
                    if features['featureName'] == feature_name:
                        feature_ip = feature_server['server_ip']
                        feature_port = features['port']

                        try:
                            print(f' Connecting to feature: {feature_name}')
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.connect((feature_ip, feature_port))
                            sock.send(serialize_msg('CONNECT_CLIENT', connect_client))

                            res = sock.recv(4096)
                            data = parse_msg(res, messenger_pb2.ConnectionResponse)[2]

                            if data['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                                yellow(f" Already subscribed to {feature_name} on {feature_ip}:{feature_port}")
                            elif data['result'] == 'CONNECTED':
                                green(f" Connected to {feature_name} on {feature_ip}:{feature_port}")
                                self.feature_sockets[feature_name] = sock
                            else:
                                red(f" Unknown connection response for {feature_name}")
                                sock.close()
                        except Exception as e:
                            red(f" Failed to connect to {feature_name}: {e}")
                            sock.close()
                            continue

    def send(self, feature_name, msg_type, payload_dict):
        """
        Send a message to the server that hosts a given feature.
        """
        if feature_name not in self.feature_sockets:
            red(f" Feature '{feature_name}' not connected. Cannot send.")
            return

        try:
            message = serialize_msg(msg_type, payload_dict)
            self.feature_sockets[feature_name].send(message)
            green(f" Sent '{msg_type}' to '{feature_name}': {payload_dict}")
        except Exception as e:
            red(f" Error sending '{msg_type}' to '{feature_name}': {e}")
