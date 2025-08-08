import queue
import time
from typing import Literal
from utils import ConnectionHandler, parse_msg, serialize_msg, red, green, yellow, blue, ping, pong
from config import config
from protobuf import messenger_pb2

FeatureName = Literal['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES']

class ServiceBase:
    """
    Base class for backend services handling connections and messages.
    """
    def __init__(self, feature_name : FeatureName, bind_port, forwarding_port=None):
        self.feature_name = feature_name

        self.server = None
        self._running = True
        self.subscriber_dict = {}   # dict to store feature subscribers
        self.server_dict = {'192.168.1.101': {
            'serverId': 'server_2',
            'functions': {'MESSAGES': {
                'conn': None,
                'port': 6666,
            }
            }
        }} # dict to store connections to other servers
        self.bind_ip = config['address']
        self.bind_port = bind_port
        self.forwarding_port = forwarding_port

        # Check: client still active?
        self.ping_timeout = config["conn_mgmt"]["ping_timeout"]

    def handle_connections(self):
        self.server = ConnectionHandler(timeout=self.ping_timeout)
        self.server.start_server(self.bind_ip, self.bind_port)

        blue(f"Listening for {self.feature_name.upper()} connections on {self.bind_ip}:{self.bind_port}...")

        while self._running:
            # Check: client still active
            def are_clients_active():
                if len(self.subscriber_dict) == 0:
                    return
                for addr, data in list(self.subscriber_dict.items()):
                    if time.time() - data['lastActive'] > self.ping_timeout and not data['ping_sent']:
                        conn = data['conn']
                        conn.send(serialize_msg('PING', ping))
                        self.subscriber_dict[addr]['ping_sent'] = True
                        yellow(f"{self.feature_name}: Client not responding. Ping sent to {data['addr']}")
                    elif time.time() - data['lastActive'] > 2 * self.ping_timeout and data['ping_sent']:
                        hangup = messenger_pb2.HangUp()
                        hangup.reason = messenger_pb2.HangUp.Reason.TIMEOUT
                        conn = data['conn']
                        conn.send(serialize_msg('HANGUP', hangup))
                        conn.close()
                        red(f"{self.feature_name}: Client not responding to Ping. Connection closed to {data['addr']}. \n")
                        del self.subscriber_dict[addr]

            try:
                msg, addr, conn = self.server.recv_msg()

                message_name, _, data = parse_msg(msg)
            except queue.Empty:
                are_clients_active()
                continue
            are_clients_active()

            # Known client handling
            if addr in self.subscriber_dict.keys():
                # update data
                self.subscriber_dict[addr]['lastActive'] = time.time()
                self.subscriber_dict[addr]['ping_sent'] = False
                # Handle messages
                message_handled = self.handle_message_for_feature(message_name, data, conn, addr)
                if not message_handled:
                    self._handle_base_messages(message_name, data, conn, addr)

            # Unknown client handling
            else:
                # Connect new client or raise error message
                if message_name == 'CONNECT_CLIENT':
                    data['conn'] = conn
                    data['addr'] = addr
                    data['lastActive'] = time.time()
                    data['ping_sent'] = False
                    self.subscriber_dict[addr] = data
                    response = messenger_pb2.ConnectResponse()
                    response.result = messenger_pb2.ConnectResponse.Result.CONNECTED
                    conn.send(serialize_msg('CONNECTED', response))
                    green(f"{self.feature_name}: Connected with {data}. \n")
                else:
                    unsupported_message = messenger_pb2.UnsupportedMessage()
                    unsupported_message.message_name = message_name
                    conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
                    yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to unknown client {addr}. \n")


    def handle_message_for_feature(self, message_name=None, data=None, conn=None, addr=None):
        """
        Updated for each feature individually if it receives messages beyond the _handle_base_messages function
        """
        return False

    def _handle_base_messages(self, message_name=None, data=None, conn=None, addr=None):
        # Handle connection response
        if message_name == 'CONNECT_CLIENT':
            response = messenger_pb2.ConnectResponse()
            response.result = messenger_pb2.ConnectResponse.Result.IS_ALREADY_CONNECTED_ERROR
            conn.send(serialize_msg('CONNECTED', response))
            yellow(f"{self.feature_name}: {addr} already subscribed. \n")
        
        # Handle Ping-Pong
        elif message_name == 'PING':
            conn.send(serialize_msg('PONG', pong))
            green(f"{self.feature_name}: Pong answered to {addr}. \n")
        elif message_name == 'PONG':
            green(f"{self.feature_name}: Pong received from {addr} \n")
        
        # Handle Hangup
        elif message_name == 'HANGUP':
            del self.subscriber_dict[addr]
            conn.close()
            red(f"{self.feature_name}: Hangup received from {addr}. Connection closed. \n")
        
        # Handle Receive Unsupported Message
        elif message_name == 'UNSUPPORTED_MESSAGE':
            yellow(f"{self.feature_name}: Client {addr} did not support {data['messageName']}. \n")
        
        # Handle all other (unsupported) messages
        else:
            unsupported_message = messenger_pb2.UnsupportedMessage()
            unsupported_message.message_name = message_name
            conn.send(serialize_msg('UNSUPPORTED_MESSAGE', unsupported_message))
            yellow(f"{self.feature_name}: {message_name} is not supported. Error message sent to known client {addr}. \n")

            
    def stop(self):
        """Gracefully stop the feature process when client UI is closed."""
        self._running = False

        client_list_text = ""
        for addr, data in list(self.subscriber_dict.items()):
            hangup = messenger_pb2.HangUp()
            hangup.reason = messenger_pb2.HangUp.Reason.EXIT
            conn = data['conn']
            conn.send(serialize_msg('HANGUP', hangup))
            conn.close()
            client_list_text += " {data['addr']}"
        red(f"{self.feature_name}: Server is closing. Connection closed to clients{client_list_text}. \n")

        self.server.close()
