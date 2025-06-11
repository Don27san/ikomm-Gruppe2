from protobuf import messenger_pb2
from google.protobuf.json_format import MessageToDict
import socket

class DiscoveryService:
    """
    Discovery Service sends out discovery broadcasts to all participants of the private network when going online. 
    
    Parameters:
    src_addr (str): Can be removed when actually broadcasting.
    src_port (int): At which we listen to responses from our broadcast

    Returns:
    server_list (list): Servers which have responded to our broadcast containing their address and supported features.
    """

    def __init__(self, src_addr = '', src_port=4567):
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind((src_addr, src_port))
        self.server_list = []
    

    def discover_servers(self, broadcast_to_port = 9999, timeout=5):
        print(f"\033[94mDiscovering Servers for {timeout} seconds...\033[0m")
        self.discovery_socket.sendto('DISCOVER_SERVER'.encode(), ('0.0.0.0', broadcast_to_port))#Todo: Must be switched to broadcasting!

        self.discovery_socket.settimeout(timeout)
        try:
            while True: #Is only necessary in the very beginning but still runs infinitely, could be disadvantageous?
                res, addr = self.discovery_socket.recvfrom(1024)
                data = messenger_pb2.ServerAnnounce()
                data.ParseFromString(res)
                dict_data = MessageToDict(data)
                dict_data['serverIP'] = addr[0] #Append Server IPs to contact them in future calls.
                self.server_list.append(dict_data) #Not protected against duplicates yet. (Is that even a case?)

                print("Discovered: ", dict_data)
        except socket.timeout:
            self.discovery_socket.close()
            print("\033[94mDiscovery finished.\033[0m \n")
        
        return self.server_list
