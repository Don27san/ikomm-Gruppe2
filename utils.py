import messenger_pb2

# Server_Announce Payload
server_announce = messenger_pb2.ServerAnnounce()
server_announce.serverId="2"
server_announce.feature.add(featureName="LIVE_LOCATION", port=8888)
server_announce.feature.add(featureName="TYPING_INDICATOR", port=7777)

# Connect_Client Payload
connect_client = messenger_pb2.ConnectClient()
connect_client.user.userId = "user123"
connect_client.user.serverId = "server456"
connect_client.portId = 9999





# Could be used to format the payload for sending over a socket.
# def format_payload(message_name, payload):
#     purpose = str(message_name).encode('ascii')
#     serialized_payload = payload.SerializeToString()
#     payload_size = str(len(serialized_payload)).encode('ascii')    
    
#     return purpose + b' ' + payload_size + b' ' + serialized_payload + '\n'.encode('ascii')









