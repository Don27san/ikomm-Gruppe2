import queue
import time
from typing import Literal
from utils import ConnectionHandler, parse_msg, serialize_msg, red, green, yellow, blue, ping, pong
from config import config
from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT_MESSAGE']

class ServiceBase:
    def __init__(self, feature_name : FeatureName, bind_port, forwarding_port=None):
        self.feature_name = feature_name
        self.subscriber_dict = {}   # dict to store feature subscribers
        self.bind_ip = config['address']
        self.bind_port = bind_port
        self.forwarding_port = forwarding_port

        # Check: client still active?
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def handle_connections(self):
        server = ConnectionHandler(timeout=self.ping_timeout)
        server.start_server(self.bind_ip, self.bind_port)

        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while True:
            # Check: client still active
            def are_clients_active():
                if len(self.subscriber_dict) == 0:
                    return
                for subscriberIP, data in list(self.subscriber_dict.items()):
                    if time.time() - data['lastActive'] > self.ping_timeout and not data['ping_sent']:
                        conn = data['conn']
                        conn.send(serialize_msg('PING', ping))
                        self.subscriber_dict[subscriberIP]['ping_sent'] = True
                        yellow(f"{self.feature_name}: Client not responding. Ping sent to {data['addr']}")
                    elif time.time() - data['lastActive'] > 2 * self.ping_timeout and data['ping_sent']:
                        hangup = messenger_pb2.HangUp()
                        hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                        conn = data['conn']
                        conn.send(serialize_msg('HANGUP', hangup))
                        conn.close()
                        red(f"{self.feature_name}: Client not responding to Ping. Connection closed to {data['addr']}. \n")
                        del self.subscriber_dict[subscriberIP]

            try:
                msg, addr, conn = server.recv_msg()

                message_name, _, data = parse_msg(msg)
                subscriberIP = addr[0]
            except queue.Empty:
                are_clients_active()
                continue
            are_clients_active()

            # Known client handling
            if subscriberIP in self.subscriber_dict.keys():
                # update data
                self.subscriber_dict[subscriberIP]['lastActive'] = time.time()
                self.subscriber_dict[subscriberIP]['ping_sent'] = False
                # handle received message
                if message_name == 'CONNECT_CLIENT':
                    response = messenger_pb2.ConnectResponse()
                    response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
                    conn.send(serialize_msg('CONNECTED', response))
                    yellow(f"{self.feature_name}: {addr} already subscribed. \n")
                elif message_name == 'PING':
                    conn.send(serialize_msg('PONG', pong))
                    green(f"{self.feature_name}: Pong answered to {addr}. \n")
                elif message_name == 'PONG':
                    green(f"{self.feature_name}: Pong received from {addr} \n")
                elif message_name == 'HANGUP':
                    del self.subscriber_dict[subscriberIP]
                    conn.close()
                    red(f"{self.feature_name}: Hangup received from {addr}. Connection closed. \n")
                elif message_name == 'UNSUPPORTED_MESSAGE':
                    yellow(f"{self.feature_name}: Client {addr} did not support {data['messageName']}. \n")
                else:
                    unsupported_message = messenger_pb2.UnsupportedMessage()
                    unsupported_message.message_name = message_name
                    conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                    yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to known client {addr}. \n")

            # Unknown client handling
            else:
                # Connect new client or raise error message
                if message_name == 'CONNECT_CLIENT':
                    data['conn'] = conn
                    data['addr'] = addr
                    data['lastActive'] = time.time()
                    data['ping_sent'] = False
                    self.subscriber_dict[subscriberIP] = data
                    response = messenger_pb2.ConnectResponse()
                    response.result = messenger_pb2.ConnectResponse.Result.CONNECTED
                    conn.send(serialize_msg('CONNECTED', response))
                    green(f"{self.feature_name}: Connected with {data}. \n")
                else:
                    unsupported_message = messenger_pb2.UnsupportedMessage()
                    unsupported_message.message_name = message_name
                    conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                    yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to unknown client {addr}. \n")
