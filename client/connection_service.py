import socket
import time
from utils import blue, green, red, yellow, serialize_msg, parse_msg, connect_client
from protobuf import messenger_pb2

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
        blue('Connecting client to features we support ...')
        # Loops through our list of features we wanna support, returns the server IP and port for the given feature which we need to subscribe to this feature
        for feature_name in self.feature_support_list:
            for feature_server in self.server_list:
                for features in feature_server['feature']:
                    if features['featureName'] == feature_name:

                        feature_ip = feature_server['server_ip'] #IP of server hosting the feature
                        feature_port = features['port'] #Port at which feature is hosted
        
                        try:
                            print(f'Connecting to feature: {feature_name}')
                            self.feature_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            self.feature_socket.connect((feature_ip, feature_port))
                            self.feature_socket.send(serialize_msg('CONNECT_CLIENT', connect_client))  # Send connection request to feature server
                            self.feature_socket.send(serialize_msg('CONNECT_CLIENT', connect_client))  # Send connection request to feature server

                            while True: 
                                buffer = b''
                                msg, _ = self.extract_msg_from_buffer(self.feature_socket, buffer)
                                message_name, _, payload = parse_msg(msg)

                                if message_name == 'CONNECTION_RESPONSE':
                                #Handle Connection Response
                                    if payload['result'] == 'IS_ALREADY_CONNECTED_ERROR':
                                        yellow(f"Connection was established. You are already on the server's subscriber list! \n")
                                    elif payload['result'] == 'CONNECTED':
                                        green(f"{payload['result']} to {feature_name} on {feature_ip}:{feature_port}. \n")
                                    else:
                                        red(f"Unknown connection response for {feature_name} from {feature_ip}:{feature_port}. \n")
                        except Exception as e:
                            red(f"Failed to connect to {feature_name} on {feature_ip}:{feature_port}. Error: {e} \n")
                            self.feature_socket.close()
                            continue





    # Todo: Must be refactored!!
    def extract_msg_from_buffer(self, conn: socket.socket, buffer: bytes):
        while buffer.count(b' ') < 2:
            res = conn.recv(1024)
            if not res:
                raise Exception("Connection closed while reading header.")
            buffer += res

        try:
            first_space = buffer.index(b' ')
            second_space = buffer.index(b' ', first_space + 1)
            payload_length = int(buffer[first_space + 1:second_space].decode())
        except ValueError:
            raise Exception("Malformed header")

        payload_start = second_space + 1
        total_needed = payload_start + payload_length + 1  # +1 for the \n

        while len(buffer) < total_needed:
            data = conn.recv(1024)
            if not data:
                raise Exception("Connection closed while reading payload.")
            buffer += data

        if buffer[total_needed - 1] != ord('\n'):
            raise Exception("Expected newline delimiter after payload.")

        msg = buffer[:total_needed]
        buffer = buffer[total_needed:]
        return msg, buffer