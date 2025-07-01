import os
import netifaces as ni
from typing import Literal, List, TypedDict

# Config Types
Feature = Literal['TYPING_INDICATOR', 'LIVE_LOCATION']

def get_port_offset():
    """Get port offset based on user ID to avoid conflicts"""
    user_id = os.getenv('CHAT_USER_ID', 'user1')
    
    # Map user IDs to port offsets
    port_offsets = {
        'user1': 0,
        'user2': 100,  # user2 gets ports +100
        'main_client_user': 0,
        'other_user': 200,  # fallback gets ports +200
    }
    
    return port_offsets.get(user_id, 0)

class ConnMgmtConfig(TypedDict):
    discovery_port: int
    ping_timeout: int    # in seconds

class MessagingFeatureConfig(TypedDict):
    connection_port: int

class TypingFeatureConfig(TypedDict):
    server_connection_port: int
    server_forwarding_port: int
    client_typing_port: int

class LocationFeatureConfig(TypedDict):
    server_connection_port: int
    server_forwarding_port: int
    client_location_port: int
    client_expiry_time: int  # in minutes
    client_sending_interval: int  # in seconds

class ChatFeatureConfig(TypedDict):
    server_port: int

class Config(TypedDict):
    address: str
    feature_support: List[Feature]
    conn_mgmt: ConnMgmtConfig
    messaging_feature: MessagingFeatureConfig
    typing_feature: TypingFeatureConfig
    location_feature: LocationFeatureConfig
    chat_feature: ChatFeatureConfig
    



config : Config = {
    # Address based on env set in pipenv script
    'address': ni.ifaddresses('en0')[ni.AF_INET][0]['addr'] if os.getenv('APP_ENV') == 'prod' else '127.0.0.1',
    'feature_support': ['TYPING_INDICATOR', 'LIVE_LOCATION'],  # Features our client wants to support

    # Features and Ports (with user-specific offsets for client ports only)
    'conn_mgmt': {
        'discovery_port': 9999,  # Keep discovery port the same for all users
        'ping_timeout': 300,
    },

    'messaging_feature':{
        'connection_port': 6666 + get_port_offset(),
    },

    'typing_feature': {
        'server_connection_port': 7777, #Server handles client connection (no offset - shared)
        'server_forwarding_port': 7778, #Server handles event forwarding (no offset - shared)
        'client_typing_port': 7779 + get_port_offset(), #Client sends events and listens to forwardings (offset for each user)
    },

    'location_feature': {
        'server_connection_port': 8887, #Server handles client connection (no offset - shared)
        'server_forwarding_port': 8888, #Server handles location forwarding (no offset - shared)
        'client_location_port': 8889 + get_port_offset(), #Client sends locations and listens to forwardings (offset for each user)
        'client_expiry_time': 5, #in min
        'client_sending_interval': 30, # in s
    },

    'chat_feature': {
        'server_port': 6001,  # TCP port for chat service (server port stays the same)
    }
}

print(f"Local IP: {config['address']}")
user_id = os.getenv('CHAT_USER_ID', 'user1')
port_offset = get_port_offset()
if port_offset > 0:
    print(f"User: {user_id} (using port offset +{port_offset})")
else:
    print(f"User: {user_id} (using default ports)")
