import socket
import time
from utils import typing_event, blue, green, parse_msg, serialize_msg
from pynput import keyboard
from config import config
from .feature_base import FeatureBase

class TypingFeature(FeatureBase):
    
    """
    Has three purposes:
    - Establishes and maintains connection to feature server
    - Listens for keystroke events to send typing_event to feature host.
    - Listens for incoming typing_events forwarded by the server.
    """
    
    def __init__(self):
        super().__init__('TYPING_INDICATOR')  #Takes care of connection
        self.src_addr = config['address']
        self.src_port = config['typing_feature']['client_typing_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.event_list = []  # List to store typing events with timestamps
        self.last_typing_sent = 0

    # Listens for keystrokes and sends typing event to server
    def handle_typing(self):

        def send_typing_event():
            server_addr = config['address']
            server_forwarding_port = config['typing_feature']['server_forwarding_port']
            typing_event.timestamp = time.time() #Todo: This is not timezone-proof. Need to deliver "timestamptz" variant.

            self.socket.sendto(serialize_msg('TYPING_EVENT', typing_event), (server_addr, server_forwarding_port))
            print(f'\nTyping Event sent to {server_addr}:{server_forwarding_port}')

        # Reduces the frequency of typing events sent to the server
        def debounce(fn, debounce_time=1):            
            now = time.time()
            if now - self.last_typing_sent > debounce_time:
                fn()
                self.last_typing_sent = now

        # Handles key press events for alphanumeric and symbol keys
        def on_press(key):
            try:
                if isinstance(key, keyboard.KeyCode) and key.char and key.char.strip():
                    debounce(fn=send_typing_event)
            except AttributeError:
                pass
            
        # Starts listening for keyboard events
        with keyboard.Listener(on_press=on_press) as listener:
            blue('Ready to handle typing event...\n')
            listener.join()




    # Listens for incoming typing events forwarded by the server
    def handle_listening(self):
        while True:
            res, addr = self.socket.recvfrom(1024)
            data = parse_msg(res)
            green(f'Received typing_events_list from {addr[0]}:{addr[1]}')
            self.event_list = data # Update the event list with the received typing events