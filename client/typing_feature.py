import socket
import time
from protobuf import messenger_pb2
from utils import typing_event, blue, green, red, serialize_msg, parse_msg
from config import config

class TypingFeature:
    """
    Handles:
    - Sending typing events to the server (with debounce)
    - Receiving forwarded typing events from the server
    """

    def __init__(self, connector):
        self.connector = connector
        self.src_addr = config['address']
        self.src_port = config['typing_feature']['client_typing_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.gui = None
        self.last_typing_sent = 0

    def set_gui(self, gui):
        self.gui = gui

    def send_typing_event(self):
        """
        Sends a typing event to the server with debounce.
        Should be called when user is editing input.
        """
        now = time.time()
        if now - self.last_typing_sent < 1:
            return  # Debounce: only send once per second

        try:
            typing_event.timestamp = now
            server_addr = config['address']
            server_forwarding_port = config['typing_feature']['server_forwarding_port']
            self.socket.sendto(serialize_msg('TYPING_EVENT', typing_event), (server_addr, server_forwarding_port))
            self.last_typing_sent = now
            print(f"Typing event sent to {server_addr}:{server_forwarding_port}")
        except Exception as e:
            red(f"Error sending typing event: {e}")

    def handle_listening(self):
        """
        Listens for typing events forwarded by the server
        and triggers GUI update if applicable.
        """
        while True:
            try:
                res, addr = self.socket.recvfrom(1024)
                data = parse_msg(res, messenger_pb2.TypingEvents)[2]
                green(f"Received typing_events from {addr[0]}:{addr[1]}")

                if self.gui:
                    self.gui.on_typing_received()
            except Exception as e:
                red(f"Error receiving typing event: {e}")
