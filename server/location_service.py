import socket
from protobuf import messenger_pb2
from google.protobuf.json_format import ParseDict
from config import config
from utils import blue, green, yellow, red, parse_msg, serialize_msg
import time
from .service_base import ServiceBase
from utils.generate_chat_message import generate_chat_message

class LocationService(ServiceBase):
    """
    Has two purposes:
    - Listens for connections requests, stores the requester as feature subscriber. Responds by telling which port to send location_events to.
    - Handles receival, bundling and forwarding of location events to the subscriber group.
    """

    def __init__(self):
        super().__init__('LIVE_LOCATION', bind_port=config['location_feature']['server_connection_port'],
                         forwarding_port=config['location_feature']['server_forwarding_port'])
        self.location_events_list = [] #List to bundle location activities. No filtering, this is client's task!



    def handle_forwarding(self):

        def send_chatmessage(data):
            content_dict={'live_location': format_live_location(data)}

            chatmessage = generate_chat_message(
                author_user_id=data['user']['userId'],
                author_server_id=data['user']['serverId'],
                content=content_dict,
            )
            print("Initial LiveLocation Chatmessage sent to all clients.")
            return chatmessage.messageSnowflake

        addr = config['address']
        port = config['location_feature']['server_forwarding_port']
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarding_socket.bind((addr, port))

        # Listen to incoming LiveLocation
        while self._running:
            try:
                res, addr = forwarding_socket.recvfrom(1024)
                data = parse_msg(res)[2]

                # Append dict with relevant data
                data['userIP'] = addr[0]
                data['userPort'] = addr[1]
                data['messageSnowflake'] = None

                if addr[0] in self.subscriber_dict.keys():
                    self.subscriber_dict[addr[0]]['lastActive'] = time.time()

                green(f'\nReceived Live Location from {addr[0]}:{addr[1]}')

                user_found = False
                # either update location_events_list...
                for item in self.location_events_list:
                    if item["userIP"] == data['userIP']:
                        item["location"] = data['location']
                        user_found = True
                        break
                # ... or append and send chatmessage
                if not user_found:
                    try:
                        data["messageSnowflake"] = send_chatmessage(data)
                        self.location_events_list.append(data)
                    except Exception as e:
                        print("Initial Live Location could not be sent via Chatmessage.")
                    continue  # skip to the next iteration of the while loop, since initial location event is sent via Chatmessage (TCP)

                # Delete expired items in location_events_list
                if len(self.location_events_list) > 0:
                    self.location_events_list = [
                        item for item in self.location_events_list if item['expiryAt'] > time.time()
                    ]

                # Forward location_events_list to all subscribers.
                if len(self.subscriber_dict) > 0:
                    live_locations = self.format_live_locations_list()
                    for subscriberIP, data in self.subscriber_dict.items():
                        # Forward message
                        forwarding_socket.sendto(serialize_msg('LIVE_LOCATIONS', live_locations),
                                                (subscriberIP, data['udpPort']))
                        print(f"Forwarded to {subscriberIP}:{data['udpPort']}")
                else:
                    yellow('Empty subscriber_list. No forwarding of live locations. \n')
            except Exception as e:
                red(f"Error handling incoming Live Location: {e}. \n")
                continue

    def format_live_locations_list(self):
        live_locations = messenger_pb2.LiveLocations()
        for event in self.location_events_list:
            extended_live_location = live_locations.extended_live_locations.add()
            extended_live_location.live_location.CopyFrom(format_live_location(event))
            extended_live_location.messageSnowflake = event["messageSnowflake"]
        
        return live_locations

def format_live_location(data):
    user_message = ParseDict(data['user'], messenger_pb2.User())

    live_location = messenger_pb2.LiveLocation()
    live_location.user.CopyFrom(user_message)
    live_location.timestamp = data['timestamp']
    live_location.expiry_at = data['expiryAt']
    live_location.location.latitude = data['location']['latitude']
    live_location.location.longitude = data['location']['longitude']

    return live_location





    #         dict_data = MessageToDict(data)
    #         dict_data['userIP'] = addr[0]
    #         dict_data['userPort'] = addr[1]
    #         green(f'\nReceived Live Location from {addr[0]}:{addr[1]}')
    #
    #         # Update location_events_list
    #         if dict_data['userIP'] not in [item['userIP'] for item in self.location_events_list]:
    #             chatmessageId = self.send_chatmessage()
    #             dict_data['chatmessageId'] = chatmessageId
    #             self.location_events_list.append(dict_data)
    #         else:
    #             for item in self.location_events_list:
    #                 if item['userIP'] == dict_data['userIP']:
    #                     item['timestamp'] = dict_data['timestamp']
    #                     item['expiryAt'] = dict_data['expiryAt']
    #                     item['location'] = dict_data['location']
    #
    #         # Delete expired items in location_events_list -> key error
    #         if len(self.location_events_list) > 0:
    #             self.location_events_list = [
    #                 item for item in self.location_events_list if item['expiryAt'] < time.time()
    #             ]
    #
    #         # Forward typing_events_list to all subscribers.
    #         if len(self.subscriber_list) > 0:
    #
    #             for subscriber in self.subscriber_list:
    #                 print(f'Forwarded to {subscriber['subscriberIP']}:{subscriber['locationPort']}')
    #                 live_locations = self.format_live_locations_list()
    #                 # Forward message
    #                 forwarding_socket.sendto(live_locations, (subscriber['subscriberIP'], subscriber['locationPort']))
    #
    #         else:
    #             yellow('Empty subscriber_list. No forwarding of live locations.')
    #
    # def format_live_locations_list(self):
    #     live_locations = messenger_pb2.LiveLocations()
    #     for event in self.location_events_list:
    #             live_location = live_locations.live_locations.add()
    #             live_location.user.userId = event["user"]["userId"]
    #             live_location.user.serverId = event["user"]["serverId"]
    #             live_location.timestamp = event["timestamp"]
    #             live_location.expiry_at = event["expiryAt"]
    #             live_location.location = event["location"]
    #     return live_locations.SerializeToString()
    #
    # def send_chatmessage(self):
    #     chatmessage = messenger_pb2.ChatMessage()
    #     chatmessage.messageId = "chatmessage123"
    #     chatmessage.live_location =
    #
    #     return chatmessage.messageId
