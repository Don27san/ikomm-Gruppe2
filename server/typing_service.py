import socket
from protobuf import messenger_pb2
from config import config
from utils import blue, green, yellow, parse_msg, serialize_msg, ConnectionHandler
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
        bind_ip = config['address']
        bind_port = config['typing_feature']['server_connection_port']
        server = ConnectionHandler()
        server.start_server(bind_ip, bind_port)
        blue(f"Listening for TYPING_INDICATOR connections on {bind_ip}:{bind_port}...")

        while True:
            msg, addr, conn = server.recv_msg()
            
            data = parse_msg(msg)[2]
            data['subscriberIP'] = addr[0]

            connection_response = messenger_pb2.ConnectionResponse()
            if data['subscriberIP'] in [subscriber['subscriberIP'] for subscriber in self.subscriber_list]:
                # If user is already subscribed, send IS_ALREADY_CONNECTED_ERROR
                connection_response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
                yellow(f'Subscriber {":".join(map(str, addr))} already subscribed to list.')
            else:
                # If this is a fresh connection, reply with CONNECTED
                connection_response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
                green(f"\nTYPING_INDICATOR connection established with: {data}")
                self.subscriber_list.append(data)

            # Send connection response
            conn.send(serialize_msg('CONNECTION_RESPONSE', connection_response))
            
            
                
                
                


            
    def handle_forwarding(self):
        addr = config['address']
        port = config['typing_feature']['server_forwarding_port']
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarding_socket.bind((addr, port))

        #Listen to incoming typing_event
        while True:
            res, addr = forwarding_socket.recvfrom(1024)
            data = parse_msg(res)[2]
            data['userIP'] = addr[0]
            data['userPort'] = addr[1]
            green(f'\nReceived typing_event from {addr[0]}:{addr[1]}')

            # 'Upsert' typing_events_list
            if data['userIP'] not in [item['userIP'] for item in self.typing_events_list]:
                self.typing_events_list.append(data)
            else:
                for item in self.typing_events_list:
                    if item['userIP'] == data['userIP']:
                        item['timestamp'] = time.time()

            #Forward typing_events_list to all subscribers.
            if len(self.subscriber_list) > 0:

                for subscriber in self.subscriber_list:
                    print(f'Forwarded to {subscriber['subscriberIP']}:{subscriber['typingPort']}')
                    typing_events = self.format_typing_events_list()
                    # Forward message 
                    forwarding_socket.sendto(serialize_msg('TYPING_EVENTS', typing_events), (subscriber['subscriberIP'], subscriber['typingPort']))
            
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
        
        
        

