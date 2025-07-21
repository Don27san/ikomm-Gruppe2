import socket
import time
from utils import typing_event, blue, green, red, parse_msg, serialize_msg
from config import config
from .feature_base import FeatureBase
from PySide6.QtCore import QObject, Signal

class TypingFeature(FeatureBase, QObject):
    
    """
    Has three purposes:
    - Establishes and maintains connection to feature server
    - Listens for keystroke events to send typing_event to feature host.
    - Listens for incoming typing_events forwarded by the server.
    """

    typing_event_received = Signal(list)  # Signal to notify GUI about new typing events

    def __init__(self):
        super().__init__('TYPING_INDICATOR')  #Takes care of connection
        QObject.__init__(self)
        self.src_addr = config['address']
        self.src_port = config['typing_feature']['client_udp_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.event_list = []  # List to store typing events with timestamps
        self.last_typing_sent = 0


    def send_typing_event(self):
        # Wait until udp_server_port is assigned
        if self.udp_server_port is not None:
            server_addr = self.server_address
            server_forwarding_port = self.udp_server_port

            typing_event.timestamp = time.time() #Todo: This is not timezone-proof. Need to deliver "timestamptz" variant.

            self.socket.sendto(serialize_msg('TYPING_EVENT', typing_event), (server_addr, server_forwarding_port))
            print(f'Typing Event sent to {server_addr}:{server_forwarding_port}. \n')
        

    # Reduces the frequency of typing events sent to the server
    def debounce(self, fn, debounce_time=1):
        now = time.time()
        if now - self.last_typing_sent > debounce_time:
            fn()
            self.last_typing_sent = now

    # Handles key press events for alphanumeric and symbol keys
    def on_press(self, key):
        try:
            self.debounce(fn=self.send_typing_event)
        except AttributeError:
            pass
            
        # Starts listening for keyboard events
        # listener = keyboard.Listener(on_press=on_press)
        # listener.start()
        # while self._running:
        #     time.sleep(1)
        # listener.stop()

        # with keyboard.Listener(on_press=on_press) as listener:
        #     blue('Ready to handle typing event...\n')
        #     listener.join()




    # Listens for incoming typing events forwarded by the server
    def handle_listening(self):
        while self._running:
            res, addr = self.socket.recvfrom(1024)
            data, _, payload = parse_msg(res)
            self.last_msg_received_time = time.time()
            green(f'Received typing_events_list from {addr[0]}:{addr[1]}')
            self.event_list = payload.get('typingEvents', [])  # Update the event list with the received typing events

            print(self.event_list)
            self.typing_event_received.emit(self.event_list)  # Emit the signal with the typing events
