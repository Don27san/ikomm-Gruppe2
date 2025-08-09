import os
import socket
from typing import Literal, List, TypedDict

def get_local_ip():
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

# Config Types
Feature = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES']

class ConnMgmtConfig(TypedDict):
    discovery_port: int
    ping_timeout: int    # in seconds

class MessagingFeatureConfig(TypedDict):
    server_connection_port: int

class ChatFeatureConfig(TypedDict):
    server_connection_port: int

class TypingFeatureConfig(TypedDict):
    server_connection_port: int
    server_forwarding_port: int
    client_udp_port: int

class LocationFeatureConfig(TypedDict):
    server_connection_port: int
    server_forwarding_port: int
    client_udp_port: int
    client_expiry_time: int  # in minutes
    client_sending_interval: int  # in seconds

class UserConfig(TypedDict):
    userId: str
    serverId: str

class Config(TypedDict):
    address: str
    user: UserConfig
    feature_support: List[Feature]
    serverId: str
    conn_mgmt: ConnMgmtConfig
    messaging_feature: MessagingFeatureConfig
    chat_feature: ChatFeatureConfig
    typing_feature: TypingFeatureConfig
    location_feature: LocationFeatureConfig
    



config : Config = {
    # Address based on env set in pipenv script
    # Change here for your local setup
    'address': get_local_ip(),
    'user': {
        'userId': 'user_1',
        'serverId': 'server_2'
    },
    'feature_support': ['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES'],  # Features our client wants to support
    'serverId': 'server_2',

    # Features and Ports
    'conn_mgmt': {
        'discovery_port': 9999,
        'ping_timeout': 300,  # timeout after which the ping is sent
    },
    'chat_feature': {
        'server_connection_port': 6666, #Server handles client connection
    },

    'typing_feature': {
        'server_connection_port': 7777, #Server handles client connection
        'server_forwarding_port': 7778, #Server handles event forwarding
        'client_udp_port': 7779, #Client sends events and listens to forwardings
    },

    'location_feature': {
        'server_connection_port': 8888, #Server handles client connection
        'server_forwarding_port': 8889, #Server handles location forwarding
        'client_udp_port': 8890, #Client sends locations and listens to forwardings
        'client_expiry_time': 5, #in min
        'client_sending_interval': 10, # in s
    }
}

print(f"Local IP: {config['address']}")
