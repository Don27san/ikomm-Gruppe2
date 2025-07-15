from protobuf import messenger_pb2
from config import config

# Server_Announce Payload
server_announce = messenger_pb2.ServerAnnounce()
server_announce.serverId=config['serverId']
server_announce.feature.add(featureName="TYPING_INDICATOR", port=config['typing_feature']['server_connection_port'],
                            udpPort=config['typing_feature']['server_forwarding_port'])
server_announce.feature.add(featureName="LIVE_LOCATION", port=config['location_feature']['server_connection_port'],
                            udpPort=config['location_feature']['server_forwarding_port'])
server_announce.feature.add(featureName="MESSAGES", port=config['chat_feature']['server_connection_port'],
                            udpPort=0)

# Connect_Client Payload
connect_client = messenger_pb2.ConnectClient()
connect_client.user.userId = config['user']['userId']
connect_client.user.serverId = config['user']['serverId']

# Typing_Event Payload
typing_event = messenger_pb2.TypingEvent()
typing_event.user.userId = config['user']['userId'] #Static value, must be replaced if necessary
typing_event.user.serverId = config['user']['serverId'] #Static value, must be replaced if necessary

# LiveLocation Payload
live_location = messenger_pb2.LiveLocation()
live_location.author.userId = config['user']['userId'] #Static value, must be replaced if necessary
live_location.author.serverId = config['user']['serverId'] #Static value, must be replaced if necessary

# ChatMessage Payload
chat_message = messenger_pb2.ChatMessage()
chat_message.messageSnowflake = 123456789  # Will be replaced with proper snowflake
chat_message.author.userId = config['user']['userId'] #Static value, must be replaced if necessary
chat_message.author.serverId = config['user']['serverId'] #Static value, must be replaced if necessary

# Ping Payload
ping = messenger_pb2.Ping()

# Pong Payload
pong = messenger_pb2.Pong()