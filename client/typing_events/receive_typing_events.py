import socket

from google.protobuf.json_format import MessageToDict
from protobuf import messenger_pb2

class TypingReceiver:
    def __init__(self, src_addr='localhost', src_port=1234):
        self.src_addr = src_addr
        self.src_port = src_port
        self.typing_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.typing_socket.bind((self.src_addr, self.src_port))
        print(f'\n\033[94mListening for typing events on {self.src_addr}:{self.src_port}...\033[0m') 

        self.typing_events_list = []  # List to store typing events with timestamps  
    
    def listen_for_typing_events(self):
        while True:
            res, addr = self.typing_socket.recvfrom(1024)
            data = messenger_pb2.TypingEvents()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            print(f'\033[92mReceived Typing event from {addr[0]}:{addr[1]}\033[0m\n')
            self.typing_events_list.append(dict_data)  # Append the received typing event to the list