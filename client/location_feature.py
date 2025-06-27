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
        self.src_port = config['location_feature']['client_location_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.location_list = []  # List to store location events with timestamps
        self.last_location_sent = 0
        self.expiry_at = 0   # expiry date for location sharing

    def start_location_sharing(self):
        self.expiry_at = time.time() + 60 * config['location_feature']['client_expiry_time']

        def send_location():
            live_location.timestamp = now
            live_location.expiry_at = self.expiry_at

            # Get location
            g = geocoder.ip('me')
            if g.ok:
                live_location.location.latitude = g.latlng[0]
                live_location.location.longitude = g.latlng[1]
                # send message
                self.socket.sendto(serialize_msg('LIVE_LOCATION', live_location), (server_addr, server_forwarding_port))
                print(f'\nLive Location sent to {server_addr}:{server_forwarding_port}')
            else:
                red("Could not determine location.")

        server_addr = config['address']
        server_forwarding_port = config['location_feature']['server_forwarding_port']

        # Only send within in predefined regularity (e.g. every 30s)
        while time.time() < self.expiry_at:
            now = time.time()
            if now - self.last_location_sent > config['location_feature']['client_sending_interval']:
                # send location
                send_location()
                self.last_location_sent = now

    def handle_listening(self):
        while True:
            res, addr = self.socket.recvfrom(1024)
            data = parse_msg(res)[2]
            green(f'Received live_locations from {addr[0]}:{addr[1]}')
            self.location_list = data # Update the event list with the received location events
