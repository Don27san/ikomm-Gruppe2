import socket
import time
import geocoder
import random
import math
from PyQt5.QtCore import QObject, pyqtSignal
from utils import green, red, serialize_msg, parse_msg, live_location
from config import config
from .feature_base import FeatureBase


class LocationFeature(FeatureBase, QObject):
    # Signal to emit when location is received
    locationEventReceived = pyqtSignal(float, float, str)  # lat, lon
    """
    ...
    """

    def __init__(self):
        super().__init__('LIVE_LOCATION')
        QObject.__init__(self)
        self.src_addr = config['address']
        self.src_port = config['location_feature']['client_udp_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.src_addr, self.src_port))
        self.location_list = []  # List to store location events with timestamps
        self.last_location_sent = 0
        self.expiry_at = 0   # expiry date for location sharing

        self._running_sharing = False

    def start_location_sharing(self, recipient_userId: str=None, recipient_serverId: str=None):
        if recipient_userId is None or recipient_serverId is None:
            red(f"{self.feature_name}: No recipient specified. Location could not be shared.\n")
            return

        self._running_sharing = True
        self.expiry_at = time.time() + 60 * config['location_feature']['client_expiry_time']

        # Wait until udp_server_port is assigned
        error_printed = False
        while self.udp_server_port is None and self._running_sharing and self._running:
            if not error_printed:
                red(f"{self.feature_name}: Location cannot be shared. No server_forwarding_port received.\n")
                error_printed = True
            time.sleep(0.1)  # wait 100ms to reduce CPU load

        while time.time() < self.expiry_at and self._running and self._running_sharing:
            now = time.time()
            if now - self.last_location_sent > config['location_feature']['client_sending_interval']:
                live_location.user.userId = str(recipient_userId)
                live_location.user.serverId = str(recipient_serverId)
                live_location.timestamp = now
                live_location.expiry_at = self.expiry_at

                try:
                    g = geocoder.ip('me')
                    if g.ok:
                        synthetic_lat, synthetic_lon = synthetic_location(g.latlng[0], g.latlng[1])
                        live_location.location.latitude = synthetic_lat
                        live_location.location.longitude = synthetic_lon
                        try:
                            self.socket.sendto(serialize_msg('LIVE_LOCATION', live_location), (self.server_address, self.udp_server_port))
                            print(f'{self.feature_name}: \nLive Location sent to {self.server_address}:{self.udp_server_port}')
                        except Exception as e:
                            red(f"{self.feature_name}: Error while sending live location: {e}")
                    else:
                        red("{self.feature_name}: Could not determine location.")
                except Exception as e:
                    red(f"{self.feature_name}: Error while sending live location: {e}")
                self.last_location_sent = now

    def stop_location_sharing(self):
        self._running_sharing = False

    def handle_listening(self):
        while self._running:
            try:
                res, addr = self.socket.recvfrom(1024)
                data = parse_msg(res)[2]
                self.last_msg_received_time = time.time()
                green(f'{self.feature_name}: Received live_locations from {addr[0]}:{addr[1]}, {data}')
                self.location_list = data['extendedLiveLocations'] # Update the event list with the received location events

                for extendedLiveLocation in self.location_list:
                    recipient = extendedLiveLocation['liveLocation'].get('user', None)
                    if recipient is not None and recipient['userId'] == config['user']['userId'] and recipient['serverId'] == config['user']['serverId']:
                        lat = extendedLiveLocation['liveLocation']['location']['latitude']
                        lon = extendedLiveLocation['liveLocation']['location']['longitude']
                        author = f"{extendedLiveLocation['liveLocation']['author']['userId']}@{extendedLiveLocation['liveLocation']['author']['serverId']}"
                        self.locationEventReceived.emit(lat, lon, author)
                    
            except Exception as e:
                red(f"{self.feature_name}: Error receiving or processing data: {e}")


def synthetic_location(base_lat, base_lon, max_meters=25):
    delta_lat = random.uniform(-1, 1) * max_meters / 111_320
    delta_lon = random.uniform(-1, 1) * max_meters / (40075000 * abs(math.cos(math.radians(base_lat))) / 360)
    return base_lat + delta_lat, base_lon + delta_lon
