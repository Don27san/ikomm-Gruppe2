config = {
    'address': '127.0.0.1',
    'feature_support': ['TYPING_INDICATOR', 'LIVE_LOCATION'],

    'conn_mgmt': {
        'discovery_port': 9999,
    },

    'messaging_feature': {
        'connection_port': 6666,
    },

    'typing_feature': {
        'server_connection_port': 7777,
        'server_forwarding_port': 7778,
        'client_typing_port': 7780,  # 改一个新端口
    },

    'location_feature': {
        'server_connection_port': 8887,
        'server_forwarding_port': 8888,
        'client_location_port': 8890,  # 改一个新端口
        'client_expiry_time': 5,
        'client_sending_interval': 30,
    }
}
