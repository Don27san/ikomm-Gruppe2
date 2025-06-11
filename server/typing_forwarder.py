import socket
import time
from protobuf import messenger_pb2
from google.protobuf.json_format import MessageToDict

class TypingForwarder:
    def __init__(self, src_addr='localhost', src_port=7778, subscriber_list=[{'subscriberIP': 'localhost', 'subscriberPort': 1234}]):
        self.src_addr = src_addr
        self.src_port = src_port
        self.last_executed = 0
        self.forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.forwarding_socket.bind((self.src_addr, self.src_port))
        
        self.subscriber_list = subscriber_list #List of users who have subscribed to the typing indicator feature
        self.typing_events_list = [] #stores most recent incoming typing events. No filtering happens here.
    
    def handle_forwarding(self):
        print(f'\033[94mReady to forward typing_events...\033[0m\n')

        #Listen to incoming typing_event
        while True:
            res, addr = self.forwarding_socket.recvfrom(1024)
            data = messenger_pb2.TypingEvent()
            data.ParseFromString(res)
            dict_data = MessageToDict(data)
            dict_data['userIP'] = addr[0]
            dict_data['userPort'] = addr[1]
            print(f'Received Typing event from {addr[0]}:{addr[1]}')

            #Either add user to event list or just updating timestamp when already in the list
            if dict_data['userIP'] not in [item['userIP'] for item in self.typing_events_list]:
                self.typing_events_list.append(dict_data)
            else:
                for item in self.typing_events_list:
                    if item['userIP'] == dict_data['userIP']:
                        item['timestamp'] = time.time()

            #Forward updated typing_events_list to all subscribers.
            for subscriber in self.subscriber_list:
                print(f'Forwarded to {subscriber['subscriberIP']}:{subscriber['subscriberPort']}\n')
                typing_events = self.format_typing_events_list()
                
                self.forwarding_socket.sendto(typing_events, (subscriber['subscriberIP'], subscriber['subscriberPort']))
                

    def format_typing_events_list(self):
        typing_events = messenger_pb2.TypingEvents()
        for event in self.typing_events_list:
                typing_event = typing_events.typing_events.add()
                typing_event.user.userId = event["user"]["userId"]
                typing_event.user.serverId = event["user"]["serverId"]
                typing_event.timestamp = event["timestamp"]
        return typing_events.SerializeToString()


        
        
            

            
            
            

        