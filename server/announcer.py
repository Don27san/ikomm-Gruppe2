import socket
from utils import server_announce

class AnnouncingService:
    """
    Announcing Service listens to server discovery calls and responds with the features which it supports
    
    Parameters:
    src_addr (str): IP Address of the server
    src_port (int): At which we listen for broadcasted discovery calls
    """

    def __init__(self, src_addr='localhost', src_port=9999):
        self.src_addr = src_addr
        self.src_port = src_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.src_addr, self.src_port))


    def announce_server(self):
        print(f'\033[94mListening for discovery requests at {self.src_addr}:{self.src_port}...\033[0m \n')

        while True: #Exception handling missing
            res, addr = self.server.recvfrom(1024)
            data = res.decode()
            if data == 'DISCOVER_SERVER':
                print(f"Received discovery request from {addr[0]}:{addr[1]}")
                self.server.sendto(server_announce.SerializeToString(), addr)
                print(f"Announced server features back to {addr[0]}:{addr[1]}\n")
                



            