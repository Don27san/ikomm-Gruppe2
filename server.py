import socket
import messenger_pb2
from utils import server_announce
import threading
from google.protobuf.json_format import MessageToDict

class Server:
    def __init__(self, src_addr = 'localhost'):
        self.src_addr = src_addr
        self.typing_indicator_subscribers = []
    
    def announce_server(self, port=9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.src_addr, port))
        print(f'\033[94mListening for discovery requests at {self.src_addr}:{port}...\033[0m \n')

        while True: #Exception handling missing
            res, addr = self.server.recvfrom(1024)
            data = res.decode()
            if data == 'DISCOVER_SERVER':
                self.server.sendto(server_announce.SerializeToString(), addr)

            print(f"Received discovery request from {addr}")

    # Listens for typing_indicator connection requests to store the requester as broadcast subscribers. After that we tell the user a dedicated port in which we receive typing events and then close the connection. The actual receive->broadcast logic will be handled in a separate function.
    def typing_indicator_subscription(self, port=7777):
        
        typing_indicator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        typing_indicator_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        typing_indicator_socket.bind((self.src_addr, port))
        typing_indicator_socket.listen(5)
        
        print(f"\033[94mListening for Typing Indicator Subscription Requests on port {port}...\033[0m \n")
        while True:
            conn, addr = typing_indicator_socket.accept()
            res = conn.recv(1024)
            data = messenger_pb2.ConnectClient()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            self.typing_indicator_subscribers.append(dict_data)
            self.typing_indicator_subscribers.append(dict_data)

            #Todo: Bis hierhin weiß server, wohin er typing events weiterleiten soll. Er hat aber den clients noch nicht gesagt, wo sie ihr typing event via UDP hinschicken müssen. Hier fehlt also noch die connection response.

            conn.close() #No further communication expected after subscribing to the typing indicator feature.

            
            print(f"\033[92mSubscription established with: {self.typing_indicator_subscribers}\033[0m")
            


test = Server(src_addr='localhost')
threading.Thread(target=test.announce_server, daemon=True).start()
test.typing_indicator_subscription()  # This runs on the main thread