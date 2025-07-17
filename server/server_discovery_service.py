import socket
from utils import red, blue, parse_msg, serialize_msg
from config import config
import os
import netifaces as ni

class ServerDiscoveryService:
    """
    Server Discovery Service - exactly like client DiscoveryService but for servers.
    Sends out discovery broadcasts to find other servers in the network.

    Returns:
    server_list (list): Servers which have responded to our broadcast containing their address and supported features.
    """

    def __init__(self):
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.bind(('', 0))  # pick arbitrary port cuz we dont care.
        self.server_list = []
    

    def discover_servers(self, timeout=2):
        blue(f"Server discovering other servers at port {config['conn_mgmt']['discovery_port']} for {timeout}s ...")
        addr = self._get_broadcast_ip() if os.getenv('APP_ENV') == 'prod' else '127.0.0.1'   # Actual broadcast address of your active network interface using netiface

        # Broadcast discovery request to entire local network.
        self.discovery_socket.sendto(serialize_msg('DISCOVER_SERVER'), (addr, config['conn_mgmt']['discovery_port']))

        self.discovery_socket.settimeout(timeout)
        try:
            while True:
                res, addr = self.discovery_socket.recvfrom(1024)
                payload = parse_msg(res)[2]  # Get the payload of the received message
                
                # Filter out our own server announcement (similar to client but for servers)
                if payload.get('serverId') != config.get('serverId'):
                    payload['server_ip'] = addr[0]  # Append Server IPs to contact them there in future calls.
                    self.server_list.append(payload)
                    print("Discovered server: ", payload)
                else:
                    print("Ignoring own server announcement")

        except socket.timeout:
            self.discovery_socket.close()
            if not self.server_list:
                blue("No other servers found on the network.")
            else:
                blue(f"Server discovery finished. Found {len(self.server_list)} servers.\n")
        
        return self.server_list

    def _get_broadcast_ip(self, interface='en0'):
        """
        Replaces <broadcast> with the actual broadcast address of your active network interface using netiface
        """
        try:
            return ni.ifaddresses(interface)[ni.AF_INET][0]['broadcast']
        except Exception as e:
            red(f"Could not determine broadcast address: {e}")
            return None
