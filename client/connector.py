import socket
from utils import connect_client

class ConnectionService:
    """
    Connection Service goes through our supported feature-list and establishes a connection with the discovered servers hosting these features.
    
    Parameters:
    feature_support_list (list): The features which we support
    server_list (list): The servers returned by our DiscoveryService.


    """
    def __init__(self, feature_support_list=[], server_list = []):
        self.feature_support_list = feature_support_list
        self.server_list = server_list

    def connect_client(self):
        print('\033[94mConnecting client to features: ', ", ".join(self.feature_support_list), '\033[0m')

        # Loops through our list of features we wanna support, returns the server IP and port for the given feature which we need to subscribe to this feature
        for feature_name in self.feature_support_list:
            for server in self.server_list:
                for features in server['feature']:
                    if features['featureName'] == feature_name:

                        feature_server_ip = server['serverIP']
                        feature_port = features['port']
        
                        try:
                            self.feature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.feature_socket.connect((feature_server_ip, feature_port))
                            self.feature_socket.send(connect_client.SerializeToString())

                            print(f"\033[92mConnected to {feature_name} on {feature_server_ip}:{feature_port}.\033[0m")
                        except Exception as e:
                            print(f"\033[91mFailed to connect to {feature_name} on {feature_server_ip}:{feature_port}. Error: {e}\033[0m")
                            continue