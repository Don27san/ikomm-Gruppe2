import socket
from protobuf import messenger_pb2
from config import config
from utils import blue, green, yellow, parse_msg, serialize_msg
import time
from .service_base import ServiceBase

class TypingService(ServiceBase):
    """
    Has two purposes:
    - Listens for connections requests, stores the requester as feature subscriber. Responds by telling which port to send typing_events to.
    - Handles receival, bundling and forwarding of typing events to the subscriber group.
    """

    def __init__(self):
        super().__init__('TYPING_INDICATOR', bind_port=config['typing_feature']['server_connection_port'],
                         forwarding_port=config['typing_feature']['server_forwarding_port'])
        self.typing_events_list = [] #List to bundle typing activities. No filtering, this is client's task!

            
    def handle_forwarding(self):
        addr = config['address']
        port = config['typing_feature']['server_forwarding_port']
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarding_socket.bind((addr, port))

        #Listen to incoming typing_event
        while self._running:
            res, addr = forwarding_socket.recvfrom(1024)
            data = parse_msg(res)[2]
            data['userIP'] = addr[0]
            data['userPort'] = addr[1]

            # Update last active:
            author_is_subscribed = False
            for subscriber_addr, item in self.subscriber_dict.items():
                if addr[0] == subscriber_addr[0] and addr[1] == item['udpPort']:
                    self.subscriber_dict[subscriber_addr]['lastActive'] = time.time()
                    author_is_subscribed = True
                    break

            green(f'\nReceived typing_event from {addr[0]}:{addr[1]}')
            # Check if author is subscribed
            if not author_is_subscribed:
                yellow(f"Author {addr[0]}:{addr[1]} is not subscribed to TYPING INDICATOR.")

            # 'Upsert' typing_events_list
            if data['userIP'] not in [item['userIP'] for item in self.typing_events_list]:
                self.typing_events_list.append(data)
            else:
                for item in self.typing_events_list:
                    if item['userIP'] == data['userIP']:
                        item['timestamp'] = time.time()

            #Forward typing_events_list to all subscribers.
            if len(self.subscriber_dict) > 0:

                for subscriber_addr, data in self.subscriber_dict.items():
                    try:
                        print(f"Forwarded to {subscriber_addr[0]}:{data['udpPort']}")
                        typing_events = self.format_typing_events_list()
                        # Forward message
                        forwarding_socket.sendto(serialize_msg('TYPING_EVENTS', typing_events), (subscriber_addr[0], data['udpPort']))
                    except Exception as e:
                        yellow(f"Error forwarding typing_events to {subscriber_addr[0]}:{data['udpPort']}: {e}")

            else:
                yellow('Empty subscriber_list. No forwarding of typing_events.')

    def format_typing_events_list(self):
        typing_events = messenger_pb2.TypingEvents()
        for event in self.typing_events_list:
                typing_event = typing_events.typing_events.add()
                typing_event.user.userId = event["user"]["userId"]
                typing_event.user.serverId = event["user"]["serverId"]
                typing_event.timestamp = event["timestamp"]
        return typing_events
        
        
        

