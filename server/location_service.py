import socket
from protobuf import messenger_pb2
from google.protobuf.json_format import ParseDict
from config import config
from utils import blue, green, yellow, red, parse_msg, serialize_msg
import time
from .service_base import ServiceBase
from utils.generate_chat_message import generate_chat_message
from .chat_service import ChatService

class LocationService(ServiceBase):
    """
    Server-side feature that receives, aggregates, and forwards live location updates.

    The service accepts UDP live-location packets from clients, keeps a short-lived
    in-memory list of the latest locations per (author, recipient) pair, and
    forwards batched updates to all subscribed clients. On the first update from a
    sender/recipient pair, the service also emits a chat message (via
    `ChatService`) that carries an initial `LiveLocation` so recipients can anchor
    the stream.

    Attributes
    ----------
    location_events_list : list[dict]
        Rolling cache of the latest live-location events. Each item contains the
        author and recipient descriptors, latest coordinates, expiry, timestamps,
        source IP/port, and the associated `messageSnowflake`.
    chat_service : ChatService
        Reference to the chatservice to create and route the initial chat message that anchors a
        live-location stream for a (author, recipient) pair.
    subscriber_dict : dict
        (Inherited from `ServiceBase`) Active subscribers keyed by (ip, tcp_port)
        with metadata like UDP port and `lastActive` timestamp.
    _running : bool
        (Inherited) Main loop guard; set to `False` to stop the service.
    forwarding_port : int
        (Configured) UDP port on which live location updates are sent and received.

    Methods
    -------
    __init__(chat_service: ChatService):
        Initialize the service, ports, caches, and chat-service dependency.
    handle_forwarding():
        Main UDP receive/forward loop. Ingests client updates, refreshes the
        rolling cache, sends an initial chat message for new streams, prunes
        expired entries, and forwards the batched `LiveLocations` to each
        subscriber.
    format_live_locations_list() -> messenger_pb2.LiveLocations:
        Build a protobuf message containing the current batch of extended live
        locations (including `messageSnowflake` references) for forwarding.
    """

    def __init__(self, chat_service: ChatService):
        super().__init__('LIVE_LOCATION', bind_port=config['location_feature']['server_connection_port'],
                         forwarding_port=config['location_feature']['server_forwarding_port'])
        self.location_events_list = [] #List to bundle location activities. No filtering, this is client's task!
        self.chat_service = chat_service

    def handle_forwarding(self):

        def send_chatmessage(data):
            content_dict={'live_location': format_live_location(data)}
            recipient_type, recipient_data = extract_recipient(data)

            chatmessage = generate_chat_message(
                author_user_id=data['author']['userId'],
                author_server_id=data['author']['serverId'],
                recipient={recipient_type: recipient_data},
                content=content_dict
            )
            self.chat_service.route_message(chatmessage)

            print("Initial LiveLocation Chatmessage sent to recipient.")
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

                # Update last active:
                author_is_subscribed = False
                for subscriber_addr, item in self.subscriber_dict.items():
                    if addr[0] == subscriber_addr[0] and addr[1] == item['udpPort']:
                        self.subscriber_dict[subscriber_addr]['lastActive'] = time.time()
                        author_is_subscribed = True
                        break

                green(f'\nReceived Live Location from {addr[0]}:{addr[1]}')
                # Check if author is subscribed
                if not author_is_subscribed:
                    yellow(f"Author {addr[0]}:{addr[1]} is not subscribed to LIVE LOCATIONs.")

                user_found = False
                # either update location_events_list...
                for item in self.location_events_list:
                    if item["userIP"] == data['userIP'] and item['userPort'] == data['userPort'] and extract_recipient(item) == extract_recipient(data):
                        item["location"] = data['location']
                        item["expiryAt"] = data["expiryAt"]
                        item["timestamp"] = data["timestamp"]
                        user_found = True
                        break
                # ... or append and send chatmessage
                if not user_found:
                    try:
                        data["messageSnowflake"] = send_chatmessage(data)
                        self.location_events_list.append(data)
                    except Exception as e:
                        print(f"Initial Live Location could not be sent via Chatmessage: {e}.")
                    continue  # skip to the next iteration of the while loop, since initial location event is sent via Chatmessage (TCP)

                # Delete expired items in location_events_list
                if len(self.location_events_list) > 0:
                    self.location_events_list = [
                        item for item in self.location_events_list if item['expiryAt'] > time.time()
                    ]

                # Forward location_events_list to all subscribers.
                if len(self.subscriber_dict) > 0:
                    live_locations = self.format_live_locations_list()
                    for subscriber_addr, data in self.subscriber_dict.items():
                        # Forward message
                        forwarding_socket.sendto(serialize_msg('LIVE_LOCATIONS', live_locations),
                                                (subscriber_addr[0], data['udpPort']))
                        print(f"Forwarded to {subscriber_addr[0]}:{data['udpPort']}")
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
    live_location = messenger_pb2.LiveLocation()

    author_message = ParseDict(data['author'], messenger_pb2.User())
    recipient_type, recipient_data = extract_recipient(data)
    if recipient_type == 'user':
        recipient_message = ParseDict(recipient_data, messenger_pb2.User())
        live_location.user.CopyFrom(recipient_message)
    elif recipient_type == 'group':
        recipient_message = ParseDict(recipient_data, messenger_pb2.Group())
        live_location.group.CopyFrom(recipient_message)
    elif recipient_type == 'userOfGroup':
        recipient_message = ParseDict(recipient_data, messenger_pb2.ChatMessage.UserOfGroup())
        live_location.userOfGroup.CopyFrom(recipient_message)
    else:
        red("Unknown or missing recipient type in data")

    live_location.author.CopyFrom(author_message)
    live_location.timestamp = data['timestamp']
    live_location.expiry_at = data['expiryAt']
    live_location.location.latitude = data['location']['latitude']
    live_location.location.longitude = data['location']['longitude']

    return live_location

def extract_recipient(data_dict):
    """
    Extracts the recipient type and recipient data from a dictionary
    converted from a protobuf ChatMessage using MessageToDict.

    Args:
        data_dict (dict): Dictionary version of a ChatMessage.

    Returns:
        tuple: (recipient_type: str or None, recipient_data: dict or None)
    """
    recipient_keys = ['user', 'group', 'userOfGroup']
    for key in recipient_keys:
        if key in data_dict:
            return key, data_dict[key]
    return None, None
