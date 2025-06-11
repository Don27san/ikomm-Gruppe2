import socket
from google.protobuf.json_format import MessageToDict
from protobuf import messenger_pb2

class TypingSubscriber:
    """
    Listens for typing_indicator connection requests to store the requester as broadcast subscribers. Responds by telling subscribers which port to send typing_events to.

    Parameters:
    src_addr (str): IP Address of the server
    src_port (int): At which we listen for broadcasted discovery calls
    """
    def __init__(self, src_addr='localhost', src_port=7777):
        self.src_addr = src_addr
        self.src_port = src_port
        self.typing_subscribers = []
        self.typing_subscriber_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.typing_subscriber_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.typing_subscriber_socket.bind((self.src_addr, self.src_port))
        self.typing_subscriber_socket.listen(5)

    def listen_for_subscription_requests(self):
        print(f"\033[94mListening for typing subscription requests on {self.src_addr}:{self.src_port}...\033[0m \n")
        while True:
            conn, addr = self.typing_subscriber_socket.accept()
            res = conn.recv(1024)
            data = messenger_pb2.ConnectClient()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            dict_data['subscriberIP'] = addr[0]
            dict_data['subscriberPort'] = addr[1]
            self.typing_subscribers.append(dict_data)
            conn.send(b'Hey there you can send your typing event to us at port blablabla')
        
            

            #Todo: Bis hierhin weiß server, wohin er typing events weiterleiten soll. Er hat aber den clients noch nicht gesagt, wo sie ihr typing event via UDP hinschicken müssen. Hier fehlt also noch die connection response.
            print(f"\033[92mTyping Subscription established with: {dict_data}\033[0m \n")
            conn.close() #No further communication expected after subscribing to the typing indicator feature.

            
            

