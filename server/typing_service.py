import socket
from google.protobuf.json_format import MessageToDict
from protobuf import messenger_pb2
from config import config
from utils import blue, green, yellow
import time

class TypingService:
    """
    Has two purposes:
    - Listens for connections requests, stores the requester as feature subscriber. Responds by telling which port to send typing_events to.
    - Handles receival, bundling and forwarding of typing events to the subscriber group.
    """

    def __init__(self):
        self.subscriber_list = [] #List to store feature subscribers
        self.typing_events_list = [] #List to bundle typing activities. No filtering, this is client's task!

    def handle_connections(self):
        addr = config['address']
        connection_port = config['typing_feature']['server_connection_port']
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection_socket.bind((addr, connection_port))
        connection_socket.listen(5)
        
        blue(f"Listening for typing_connections on {addr}:{connection_port}...")

        while True:
            conn, addr = connection_socket.accept()
            res = conn.recv(1024)
            data = messenger_pb2.ConnectClient()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            dict_data['subscriberIP'] = addr[0]

            # If user is already subscribed, send IS_ALREADY_CONNECTED_ERROR
            if dict_data['subscriberIP'] in [subscriber['subscriberIP'] for subscriber in self.subscriber_list]:
                connection_response = messenger_pb2.ConnectionResponse()
                connection_response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
                conn.send(connection_response.SerializeToString())
                yellow(f'Subscriber {":".join(map(str, addr))} already subscribed in list.')
            # If this is a fresh connection, reply with CONNECTED
            else:
                connection_response = messenger_pb2.ConnectionResponse()
                connection_response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
                conn.send(connection_response.SerializeToString())
                self.subscriber_list.append(dict_data)
                green(f"\nTYPING_INDICATOR connection established with: {dict_data}")
                


            
    def handle_forwarding(self):
        addr = config['address']
        port = config['typing_feature']['server_forwarding_port']
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarding_socket.bind((addr, port))

        #Listen to incoming typing_event
        while True:
            res, addr = forwarding_socket.recvfrom(1024)
            data = messenger_pb2.TypingEvent()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            dict_data['userIP'] = addr[0]
            dict_data['userPort'] = addr[1]
            green(f'\nReceived typing_event from {addr[0]}:{addr[1]}')

            # 'Upsert' typing_events_list
            if dict_data['userIP'] not in [item['userIP'] for item in self.typing_events_list]:
                self.typing_events_list.append(dict_data)
            else:
                for item in self.typing_events_list:
                    if item['userIP'] == dict_data['userIP']:
                        item['timestamp'] = time.time()

            #Forward typing_events_list to all subscribers.
            if len(self.subscriber_list) > 0:

                for subscriber in self.subscriber_list:
                    print(f'Forwarded to {subscriber['subscriberIP']}:{subscriber['typingPort']}')
                    typing_events = self.format_typing_events_list()
                    # Forward message 
                    forwarding_socket.sendto(typing_events, (subscriber['subscriberIP'], subscriber['typingPort']))
            
            else:
                yellow('Empty subscriber_list. No forwarding of typing_events.')

    def format_typing_events_list(self):
        typing_events = messenger_pb2.TypingEvents()
        for event in self.typing_events_list:
                typing_event = typing_events.typing_events.add()
                typing_event.user.userId = event["user"]["userId"]
                typing_event.user.serverId = event["user"]["serverId"]
                typing_event.timestamp = event["timestamp"]
        return typing_events.SerializeToString()
        
        
        

