import socket
from utils import server_announce, blue, green
from config import config


class AnnouncementService:
    """
    Announcement Service listens to server discovery calls and responds with the features which it supports
    """

    def __init__(self):
        self.src_addr = '0.0.0.0' #Listens to incoming broadcasts from all network interfaces
        self.src_port = config['conn_mgmt']['discovery_port'] #Port specified in config file
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.src_addr, self.src_port))


    def announce_server(self):
        blue(f'Listening for discovery requests at {self.src_addr}:{self.src_port}...\n')

        while True: #Exception handling missing
            res, addr = self.server.recvfrom(1024)
            data = res.decode()
            if data == 'DISCOVER_SERVER':
                green(f"\nReceived discovery request from {addr[0]}:{addr[1]}")
                self.server.sendto(server_announce.SerializeToString(), addr)
                print(f"Announced server features back to {addr[0]}:{addr[1]}")
                



            