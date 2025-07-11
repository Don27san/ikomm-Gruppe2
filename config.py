import os
import netifaces as ni
from typing import Literal, List, TypedDict

# Config Types
Feature = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT_MESSAGE']

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
    serverId: str
    feature_support: List[Feature]
    server_id: str
    conn_mgmt: ConnMgmtConfig
    messaging_feature: MessagingFeatureConfig
    chat_feature: ChatFeatureConfig
    typing_feature: TypingFeatureConfig
    location_feature: LocationFeatureConfig
    



config : Config = {
    # Address based on env set in pipenv script
    'address': ni.ifaddresses('en0')[ni.AF_INET][0]['addr'] if os.getenv('APP_ENV') == 'prod' else '127.0.0.1',
    'user': {
        'userId': 'user_1',
        'serverId': 'ikomm_server_2'
    },
    'serverId': 'ikomm_server_2', # The ID of this server instance
    'feature_support': ['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT_MESSAGE'],  # Features our client wants to support
    'server_id': 'Server_2',  

    # Features and Ports
    'conn_mgmt': {
        'discovery_port': 9999,
        'ping_timeout': 300,
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
        'client_sending_interval': 30, # in s
    }
}

print(f"Local IP: {config['address']}")
