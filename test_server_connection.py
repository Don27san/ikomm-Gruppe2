#!/usr/bin/env python3
"""
Server-to-Server Connection Test

This script demonstrates how the server-to-server discovery and connection works.
It can be used to test the implementation by running multiple server instances.

Usage:
    # Terminal 1 - Start first server
    python test_server_connection.py --server-id server_1 --port-offset 0
    
    # Terminal 2 - Start second server  
    python test_server_connection.py --server-id server_2 --port-offset 10
    
    # Terminal 3 - Start third server
    python test_server_connection.py --server-id server_3 --port-offset 20
"""

import sys
import argparse
import threading
import time
import signal
from pathlib import Path

# Add the project root to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from server.server_discovery_service import ServerDiscoveryService
from server.server_connection_base import ServerConnectionBase
from server.announcement_service import AnnouncementService
from utils import red, blue, green, yellow
from config import config


class TestServerConnection:
    def __init__(self, server_id, port_offset=0):
        self.server_id = server_id
        self.port_offset = port_offset
        self._running = True
        
        # Update config for this test instance
        config['serverId'] = server_id
        config['chat_feature']['server_connection_port'] += port_offset
        config['typing_feature']['server_connection_port'] += port_offset
        config['typing_feature']['server_forwarding_port'] += port_offset
        config['location_feature']['server_connection_port'] += port_offset
        config['location_feature']['server_forwarding_port'] += port_offset
        
        self.announcer = None
        self.server_connector = None
        
    def start(self):
        """Start the test server with server-to-server functionality."""
        blue(f"Starting test server {self.server_id} with port offset {self.port_offset}")
        
        # Setup graceful shutdown
        def shutdown_handler(signum, frame):
            red(f"\nShutting down server {self.server_id}...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
        
        # Start announcement service
        blue(f"Server {self.server_id}: Starting announcement service...")
        self.announcer = AnnouncementService()
        threading.Thread(target=self.announcer.announce_server, daemon=True).start()
        
        # Wait a bit for announcement service to start
        time.sleep(1)
        
        # Discover other servers
        blue(f"Server {self.server_id}: Discovering other servers...")
        server_discovery = ServerDiscoveryService()
        server_list = server_discovery.discover_servers(timeout=3)
        
        if server_list:
            green(f"Server {self.server_id}: Found {len(server_list)} other servers")
            for server_info in server_list:
                print(f"  - {server_info['serverId']} at {server_info['server_ip']}")
            
            # Connect to discovered servers
            offered_features = ['TYPING_INDICATOR', 'LIVE_LOCATION', 'MESSAGES']
            self.server_connector = ServerConnectionBase(offered_features)
            
            blue(f"Server {self.server_id}: Connecting to discovered servers...")
            self.server_connector.handle_server_connections(server_list)
            
            # Wait for connections to establish
            time.sleep(2)
            
            # Show connection status
            connected_count = len(self.server_connector.connected_servers)
            if connected_count > 0:
                green(f"Server {self.server_id}: Connected to {connected_count} servers:")
                for server_id in self.server_connector.connected_servers:
                    print(f"  - Connected to {server_id}")
            else:
                yellow(f"Server {self.server_id}: No server connections established")
        else:
            blue(f"Server {self.server_id}: No other servers found")
        
        # Keep running
        blue(f"Server {self.server_id}: Running... (Press Ctrl+C to stop)")
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the test server."""
        self._running = False
        if self.server_connector:
            self.server_connector.stop()
        if self.announcer:
            self.announcer.stop()
        red(f"Server {self.server_id}: Stopped")


def main():
    parser = argparse.ArgumentParser(description='Test server-to-server connections')
    parser.add_argument('--server-id', required=True, help='Unique server identifier')
    parser.add_argument('--port-offset', type=int, default=0, 
                       help='Port offset to avoid conflicts (default: 0)')
    
    args = parser.parse_args()
    
    # Validate server ID
    if not args.server_id or args.server_id.strip() == '':
        red("Error: server-id cannot be empty")
        sys.exit(1)
    
    test_server = TestServerConnection(args.server_id, args.port_offset)
    test_server.start()


if __name__ == "__main__":
    main()
