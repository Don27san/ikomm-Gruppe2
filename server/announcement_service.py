import socket
from utils import server_announce, blue, green, parse_msg, serialize_msg
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
            message_name = parse_msg(res)[0]
            if message_name == 'DISCOVER_SERVER':
                green(f"\nReceived discovery request from {addr[0]}:{addr[1]}")
                self.server.sendto(serialize_msg('SERVER_ANNOUNCE', server_announce), addr)
                print(f"Announced server features back to {addr[0]}:{addr[1]}")
                



            