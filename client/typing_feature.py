import socket
import time
from protobuf import messenger_pb2
from utils import typing_event, blue, green
from pynput import keyboard
from config import config
from google.protobuf.json_format import MessageToDict

class TypingFeature:
    
    """
    Has two purposes:
    - Listens for keystroke events to send typing_event to feature host.
    - Listens for incoming typing_events forwarded by the server.
    """
    
    def __init__(self, ):
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

            self.socket.sendto(typing_event.SerializeToString(), (server_addr, server_forwarding_port))
            print(f'\nTyping Event sent to {server_addr}:{server_forwarding_port}')

        # Reduces the frequency of typing events sent to the server
        def debounce(fn, debounce_time=1):            
            now = time.time()
            if now - self.last_typing_sent > debounce_time:
                fn()
                self.last_typing_sent = now

        # Handles key press events
        def on_press():
            try:
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
            data = messenger_pb2.TypingEvents()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            green(f'Received typing_events_list from {addr[0]}:{addr[1]}')
            self.event_list = dict_data # Update the event list with the received typing events