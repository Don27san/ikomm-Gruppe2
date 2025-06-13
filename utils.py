from protobuf import messenger_pb2
from config import config

# Server_Announce Payload
server_announce = messenger_pb2.ServerAnnounce()
server_announce.serverId="2"
server_announce.feature.add(featureName="TYPING_INDICATOR", port=config['typing_feature']['server_connection_port'])
server_announce.feature.add(featureName="LIVE_LOCATION", port=config['location_feature']['server_connection_port'])

# Connect_Client Payload
connect_client = messenger_pb2.ConnectClient()
connect_client.user.userId = "user123" #Static value, must be replaced if necessary
connect_client.user.serverId = "server456" #Static value, must be replaced if necessary
connect_client.typingPort = config['typing_feature']['client_typing_port']

# Typing_Event Payload
typing_event = messenger_pb2.TypingEvent()
typing_event.user.userId = "user123" #Static value, must be replaced if necessary
typing_event.user.serverId = "server456" #Static value, must be replaced if necessary



def red(string):
    print('\033[31m' + string + '\033[0m')

def blue(string):
    print('\033[34m' + string + '\033[0m')

def green(string):
    print('\033[32m' + string + '\033[0m')

def yellow(string):
    print('\033[93m' + string + '\033[0m')








# Could be used to format the payload for sending over a socket.
# def format_payload(message_name, payload):
#     purpose = str(message_name).encode('ascii')
#     serialized_payload = payload.SerializeToString()
#     payload_size = str(len(serialized_payload)).encode('ascii')    
    
#     return purpose + b' ' + payload_size + b' ' + serialized_payload + '\n'.encode('ascii')









