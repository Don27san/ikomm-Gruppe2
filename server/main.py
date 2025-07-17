import threading
import signal
import sys
import time

from .announcement_service import AnnouncementService
from .typing_service import TypingService
from .location_service import LocationService
from .chat_service import ChatService
from .server_discovery_service import ServerDiscoveryService
from utils import red, blue


def main():
    def shutdown_handler(signum, frame):
        red("\nGracefully shutting down...")
        typing_service.stop()
        location_service.stop()
        chat_service.stop()
        announcer.stop()
        sys.exit(0)

    # Graceful shutdown
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Listen for discovery calls and announce server
    announcer = AnnouncementService()
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Server Discovery (exactly like client main.py)
    server_discovery = ServerDiscoveryService()
    server_list = server_discovery.discover_servers()

    # Initialize services
    typing_service = TypingService()
    chat_service = ChatService()
    location_service = LocationService(chat_service=chat_service)

    # Connect each service to other servers (exactly like client pattern)
    typing_service.set_server_list_and_connect(server_list)
    chat_service.set_server_list_and_connect(server_list)
    location_service.set_server_list_and_connect(server_list)

    # Start services
    threading.Thread(target=typing_service.handle_connections, daemon=True).start()
    threading.Thread(target=typing_service.handle_forwarding, daemon=True).start()

    threading.Thread(target=chat_service.handle_connections, daemon=True).start()

    threading.Thread(target=location_service.handle_connections, daemon=True).start()
    threading.Thread(target=location_service.handle_forwarding, daemon=True).start()

    # Keep the main thread alive.
    while True:
        pass
    




if __name__ == "__main__":
    main()


