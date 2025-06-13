import socket
import os


config = {
    # Address based on env set in pipenv script
    'address': socket.gethostbyname(socket.gethostname()) if os.getenv('APP_ENV') == 'prod' else 'localhost',

    # Features and Ports
    'conn_mgmt': {
        'discovery_port': 9999,
    },

    'messaging_feature':{
        'connection_port': 6666,
    },

    'typing_feature': {
        'connection_port': 7777,
        'udp_port': 7778,
    },

    'location_feature': {
        'connection_port': 8888,
    }
}