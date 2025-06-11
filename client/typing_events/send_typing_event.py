import socket
import time
from utils import typing_event
from pynput import keyboard

class TypingEvent:
    def __init__(self, dest_addr='localhost', dest_port=7778, debounce_time=1):
        self.dest_addr = dest_addr
        self.dest_port = dest_port
        self.debounce_time = debounce_time
        self.last_executed = 0
        self.typing_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def activate(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            print('\n\033[94mReady to send typing event...\033[0m \n')
            listener.join()

    def debounce(self, fn):
        now = time.time()
        if now - self.last_executed > self.debounce_time:
            fn()
            self.last_executed = now
        
    def on_press(self, key):
        try:
            self.debounce(fn=self.send_typing_event)
            
        except AttributeError:
            pass
    
    def send_typing_event(self):
        
        typing_event.timestamp = time.time() #Todo: This is not timezone-proof. Need to deliver "timestamptz" variant.
        self.typing_socket.sendto(typing_event.SerializeToString(), (self.dest_addr, self.dest_port))
        print(typing_event)
        print(f'Typing Event sent to {self.dest_addr}:{self.dest_port}')