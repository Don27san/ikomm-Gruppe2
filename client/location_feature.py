import socket
import time
from google.protobuf.json_format import MessageToDict
from protobuf import messenger_pb2
from utils import live_location, blue, green, red, parse_msg, serialize_msg

class LocationFeature:
    """
    Handles sending and receiving live location events.

    Parameters:
    - connector: ConnectionService
    - config: dict (injected per instance)
    """

    def __init__(self, connector, config):
        self.connector = connector
        self.config = config
        self.gui = None
        self.src_addr = config['address']
        self.src_port = config['location_feature']['client_location_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.location_list = []
        self.last_location_sent = 0
        self.expiry_at = 0

    def set_gui(self, gui):
        self.gui = gui

    def send_location(self, lat, lon):
        """
        Manually triggered one-time location sharing
        """
        server_addr = self.config['address']
        server_forwarding_port = self.config['location_feature']['server_forwarding_port']

        live_location.timestamp = time.time()
        live_location.expiry_at = live_location.timestamp + 60 * self.config['location_feature']['client_expiry_time']
        live_location.location.latitude = lat
        live_location.location.longitude = lon

        try:
            self.socket.sendto(serialize_msg('LOCATION_EVENT', live_location), (server_addr, server_forwarding_port))
            print(f"Sent live location to {server_addr}:{server_forwarding_port} -> {lat}, {lon}")
        except Exception as e:
            red(f"Error sending location: {e}")

    def handle_listening(self):
        while True:
            try:
                res, addr = self.socket.recvfrom(1024)
                data = parse_msg(res, messenger_pb2.LiveLocations)[2]
                green(f"Received live_locations from {addr[0]}:{addr[1]}")
                self.location_list = data

                if self.gui:
                    for extended in data.extended_live_locations:
                        lat = extended.live_location.location.latitude
                        lon = extended.live_location.location.longitude
                        self.gui.on_location_received(lat, lon)

            except Exception as e:
                red(f"Error receiving location: {e}")
