import socket
from protobuf import messenger_pb2 # Import the generated protobuf code

class AnnouncingService:
    """
    Announcing Service listens to server discovery calls and responds with the features which it supports
    
    Parameters:
    src_addr (str): IP Address of the server
    src_port (int): At which we listen for broadcasted discovery calls
    server_id (str): The unique ID of this server.
    features (list): A list of dictionaries, where each dict has 'name' and 'port' for a feature.
                     Example: [{'name': 'TYPING_INDICATOR', 'port': 7777}, {'name': 'CHAT', 'port': 5001}]
    """

    def __init__(self, src_addr='localhost', src_port=9999, server_id="default_server", features=None):
        self.src_addr = src_addr
        self.src_port = src_port
        self.server_id = server_id
        self.features = features if features is not None else []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # For UDP broadcast listening, binding to '' or '0.0.0.0' is common for discovery
        # If client sends to specific server IP, src_addr is fine.
        # For general broadcast discovery, client sends to 255.255.255.255 or subnet broadcast.
        # Server should listen on an address that can receive these (e.g., '' for all interfaces).
        self.server.bind(('', self.src_port)) # Listen on all interfaces for discovery


    def announce_server(self):
        print(f'\033[94mListening for discovery requests on port {self.src_port}...\033[0m \n')

        while True: 
            try:
                res, addr = self.server.recvfrom(1024)
                data = res.decode()
                if data == 'DISCOVER_SERVER':
                    print(f"Received discovery request from {addr[0]}:{addr[1]}")
                    
                    # Create ServerAnnounce message dynamically
                    announce_msg = messenger_pb2.ServerAnnounce()
                    announce_msg.serverId = self.server_id
                    for feature_info in self.features:
                        feature_pb = announce_msg.feature.add()
                        feature_pb.featureName = feature_info['name']
                        feature_pb.port = feature_info['port']
                        
                    self.server.sendto(announce_msg.SerializeToString(), addr)
                    print(f"Announced server features (ID: {self.server_id}, Features: {self.features}) back to {addr[0]}:{addr[1]}\n")
            except UnicodeDecodeError:
                print(f"Received non-UTF-8 data from {addr}. Ignoring.")
            except Exception as e:
                print(f"Error in announce_server: {e}")




