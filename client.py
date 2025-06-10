import socket
import messenger_pb2
from utils import connect_client
from google.protobuf.json_format import MessageToDict


class Client:
    
    def __init__(self, src_addr = 'localhost', src_port = 5050, feature_support_list=[]):
        self.feature_support_list = feature_support_list #The list of features we want to support and connect to.
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((src_addr, src_port))
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #Allows socket to broadcast
        print(f'\033[94mCreated client socket at {src_addr} listening/sending from port {src_port}...\033[0m \n')

        #Storing the server location and feature information from our discovery broadcast
        self.server_list = []



    def discover_server(self, broadcast_to_port=9999):
        print("\033[94mDiscovering Servers...\033[0m")
        self.client.sendto('DISCOVER_SERVER'.encode(), ('localhost', broadcast_to_port))
        while True: #Is only necessary in the very beginning but still runs infinitely, could be disadvantageous?
            res, addr = self.client.recvfrom(1024)
            data = messenger_pb2.ServerAnnounce()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            dict_data['serverIP'] = addr[0] #Append Server IPs to contact them in future calls.
            self.server_list.append(dict_data) #Not protected against duplicates yet.

            print("Discovered: ", self.server_list, '\n')
            self.connect_client()

    #Send client connection request to the servers whose features we want to support.
    def connect_client(self):
        print('\033[94mConnecting client to features: ', ", ".join(self.feature_support_list), '\033[0m')

        # Loops through our list of features we wanna support, returns the server IP and port for the given feature
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
                        
                             

        

        # self.ll_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.ll_socket.connect(())
            
            

    


test = Client(src_addr='localhost', src_port=5050, feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION'])
test.discover_server()
