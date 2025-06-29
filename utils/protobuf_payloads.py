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
connect_client.location_port = config['location_feature']['client_location_port']

# Typing_Event Payload
typing_event = messenger_pb2.TypingEvent()
typing_event.user.userId = "user123" #Static value, must be replaced if necessary
typing_event.user.serverId = "server456" #Static value, must be replaced if necessary

# LiveLocation Payload
live_location = messenger_pb2.LiveLocation()
live_location.user.userId = "user123" #Static value, must be replaced if necessary
live_location.user.serverId = "server456" #Static value, must be replaced if necessary

# Ping Payload
ping = messenger_pb2.Ping()

# Pong Payload
pong = messenger_pb2.Pong()