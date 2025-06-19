import socket
import os


config = {
    # Address based on env set in pipenv script
    'address': socket.gethostbyname(socket.gethostname()) if os.getenv('APP_ENV') == 'prod' else '127.0.0.1',

    # Features and Ports
    'conn_mgmt': {
        'discovery_port': 9999,
    },

    'messaging_feature':{
        'connection_port': 6666,
    },

    'typing_feature': {
        'server_connection_port': 7777, #Server handles client connection
        'server_forwarding_port': 7778, #Server handles event forwarding
        'client_typing_port': 7779, #Client sends events and listens to forwardings
    },

    'location_feature': {
        'server_connection_port': 8887, #Server handles client connection
        'server_forwarding_port': 8888, #Server handles location forwarding
        'client_location_port': 8889, #Client sends locations and listens to forwardings
        'client_expiry_time': 5, #in min
        'client_sending_interval': 30, # in s
    }
}