from typing import Literal
from utils import ConnectionHandler, parse_msg, serialize_msg, green, yellow, blue
from config import config
from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT_MESSAGE']

class ServiceBase:
    def __init__(self, feature_name : FeatureName, bind_port):
        self.feature_name = feature_name
        self.subscriber_list = [] #List to store feature subscribers
        self.bind_ip = config['address']
        self.bind_port = bind_port  

    def handle_connections(self):
        server = ConnectionHandler()
        server.start_server(self.bind_ip, self.bind_port)

        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while True:
            msg, addr, conn = server.recv_msg()
            data = parse_msg(msg)[2]
            data['subscriberIP'] = addr[0]

            response = messenger_pb2.ConnectionResponse()

            if data['subscriberIP'] in [sub['subscriberIP'] for sub in self.subscriber_list]:
                response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
                yellow(f"{self.feature_name}: {addr} already subscribed.")
            else:
                response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
                green(f"{self.feature_name}: Connected with {data}")
                self.subscriber_list.append(data)

            conn.send(serialize_msg('CONNECTION_RESPONSE', response))
