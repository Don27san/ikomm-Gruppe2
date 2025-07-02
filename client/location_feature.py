import socket
import time
import geocoder
from utils import green, red, serialize_msg, parse_msg, live_location
from config import config
from .feature_base import FeatureBase

class LocationFeature(FeatureBase):
    """
    ...
    """

    def __init__(self):
        super().__init__('LIVE_LOCATION')
        self.src_addr = config['address']
        self.src_port = config['location_feature']['client_udp_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.location_list = []  # List to store location events with timestamps
        self.last_location_sent = 0
        self.expiry_at = 0   # expiry date for location sharing

        self._running_sharing = False

    def start_location_sharing(self):
        self._running_sharing = True
        self.expiry_at = time.time() + 60 * config['location_feature']['client_expiry_time']

        # Wait until udp_server_port is assigned
        error_printed = False
        while self.udp_server_port is None and self._running_sharing and self._running:
            if not error_printed:
                red(f"Location cannot be shared. No server_forwarding_port received.\n")
                error_printed = True
            time.sleep(0.1)  # wait 100ms to reduce CPU load

        server_addr = self.server_address
        server_forwarding_port = self.udp_server_port

        while time.time() < self.expiry_at and self._running and self._running_sharing:
            now = time.time()
            if now - self.last_location_sent > config['location_feature']['client_sending_interval']:
                live_location.timestamp = now
                live_location.expiry_at = self.expiry_at

                try:
                    g = geocoder.ip('me')
                    if g.ok:
                        live_location.location.latitude = g.latlng[0]
                        live_location.location.longitude = g.latlng[1]
                        try:
                            self.socket.sendto(serialize_msg('LIVE_LOCATION', live_location), (server_addr, server_forwarding_port))
                            print(f'\nLive Location sent to {server_addr}:{server_forwarding_port}')
                        except Exception as e:
                            red(f"Error while sending live location: {e}")
                    else:
                        red("Could not determine location.")
                except Exception as e:
                    red(f"Error while sending live location: {e}")
                self.last_location_sent = now

    def stop_location_sharing(self):
        self._running_sharing = False

    def handle_listening(self):
        while self._running:
            try:
                res, addr = self.socket.recvfrom(1024)
                data = parse_msg(res)[2]
                self.last_msg_received_time = time.time()
                green(f'Received live_locations from {addr[0]}:{addr[1]}')
                self.location_list = data # Update the event list with the received location events
            except Exception as e:
                red(f"Error receiving or processing data: {e}")
