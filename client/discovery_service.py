from protobuf import messenger_pb2
from google.protobuf.json_format import MessageToDict
import socket
from config import config
from utils import blue
import os

class DiscoveryService:
    """
    Discovery Service sends out discovery broadcasts to all participants of the private network when going online. 

    Returns:
    server_list (list): Servers which have responded to our broadcast containing their address and supported features.
    """

    def __init__(self):
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', 0)) #pick arbitrary port cuz we dont care.
        self.server_list = []
    

    def discover_servers(self, timeout=5):
        blue(f'Discovering servers at port {config['conn_mgmt']['discovery_port']} for {timeout}s ...')
        # Broadcast discovery request to entire local network.
        addr = '<broadcast>' if os.getenv('APP_ENV') == 'prod' else '127.0.0.1' #We only broadcast when in prod. Otherwise we push via localhost for testing.
        self.discovery_socket.sendto('DISCOVER_SERVER'.encode(), (addr, config['conn_mgmt']['discovery_port']))

        self.discovery_socket.settimeout(timeout)
        try:
            while True:
                res, addr = self.discovery_socket.recvfrom(1024)
                data = messenger_pb2.ServerAnnounce()
                data.ParseFromString(res)
                dict_data = MessageToDict(data)
                dict_data['server_ip'] = addr[0] #Append Server IPs to contact them there in future calls.
                self.server_list.append(dict_data) #Not protected against duplicates yet. (Is that even a case?)

                print("Discovered: ", dict_data)

        except socket.timeout:
            self.discovery_socket.close()
            blue("Discovery finished.\n")
        
        return self.server_list
