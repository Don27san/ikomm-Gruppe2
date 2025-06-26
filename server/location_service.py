import socket
from protobuf import messenger_pb2
from google.protobuf.json_format import ParseDict
from config import config
from utils import blue, green, yellow, parse_msg, serialize_msg
import time

class LocationService:
    """
    Has two purposes:
    - Listens for connections requests, stores the requester as feature subscriber. Responds by telling which port to send location_events to.
    - Handles receival, bundling and forwarding of location events to the subscriber group.
    """

    def __init__(self):
        self.subscriber_list = [] #List to store feature subscribers
        self.location_events_list = [] #List to bundle location activities. No filtering, this is client's task!

    def handle_connections(self):
        addr = config['address']
        connection_port = config['location_feature']['server_connection_port']
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection_socket.bind((addr, connection_port))
        connection_socket.listen(5)

        blue(f"Listening for location_connections on {addr}:{connection_port}...")

        while True:
            conn, addr = connection_socket.accept()
            res = conn.recv(1024)
            data = parse_msg(res)[2]
            data['subscriberIP'] = addr[0]

            connection_response = messenger_pb2.ConnectionResponse()
            if data['subscriberIP'] in [subscriber['subscriberIP'] for subscriber in self.subscriber_list]:
                # If user is already subscribed, send IS_ALREADY_CONNECTED_ERROR
                connection_response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
                yellow(f'Subscriber {":".join(map(str, addr))} already subscribed to list.')
            else:
                # If this is a fresh connection, reply with CONNECTED
                connection_response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
                green(f"\nLOCATION_SERVICE connection established with: {data}")
                self.subscriber_list.append(data)

            # Send connection response
            conn.send(serialize_msg('CONNECTION_RESPONSE', connection_response))

    def handle_forwarding(self):

        def send_chatmessage(data):
            chatmessage = messenger_pb2.ChatMessage()
            chatmessage.messageSnowflake = int(time.time() * 1000)  # Generate snowflake
            chatmessage.live_location.CopyFrom(format_live_location(data))
            print("Initial LiveLocation Chatmessage sent to all clients.")
            return str(chatmessage.messageSnowflake)

        addr = config['address']
        port = config['location_feature']['server_forwarding_port']
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        forwarding_socket.bind((addr, port))

        # Listen to incoming LiveLocation
        while True:
            res, addr = forwarding_socket.recvfrom(1024)
            data = parse_msg(res)[2]

            # Append dict with relevant data
            data['userIP'] = addr[0]
            data['userPort'] = addr[1]
            data['chatMessageID'] = None

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
                chatmessageID = send_chatmessage(data)
                data["chatMessageID"] = chatmessageID
                self.location_events_list.append(data)
                continue  # skip to the next iteration of the while loop, since initial location event is sent via Chatmessage (TCP)

            # Delete expired items in location_events_list
            if len(self.location_events_list) > 0:
                self.location_events_list = [
                    item for item in self.location_events_list if item['expiryAt'] > time.time()
                ]

            # Forward location_events_list to all subscribers.
            if len(self.subscriber_list) > 0:
                live_locations = self.format_live_locations_list()
                for subscriber in self.subscriber_list:
                    # Forward message
                    forwarding_socket.sendto(serialize_msg('LIVE_LOCATIONS', live_locations),
                                            (subscriber['subscriberIP'], subscriber['locationPort']))
                    print(f'Forwarded to {subscriber['subscriberIP']}:{subscriber['locationPort']}')
            else:
                yellow('Empty subscriber_list. No forwarding of live locations.')

    def format_live_locations_list(self):
        live_locations = messenger_pb2.LiveLocations()
        for event in self.location_events_list:
            extended_live_location = live_locations.extended_live_locations.add()
            extended_live_location.live_location.CopyFrom(format_live_location(event))
            extended_live_location.chatmessageID = event["chatMessageID"]
        
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
