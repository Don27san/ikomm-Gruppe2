import threading
import signal
import sys
import time

from .announcement_service import AnnouncementService
from .typing_service import TypingService
from .location_service import LocationService
from utils import red


def main():
    def shutdown_handler(signum, frame):
        red("\nGracefully shutting down...")
        typing_service.stop()
        location_service.stop()
        announcer.stop()
        sys.exit(0)

    # Graceful shutdown
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Listen for discovery calls and announce server
    announcer = AnnouncementService()
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Typing Indicator Feature
    typing_service= TypingService()
    threading.Thread(target=typing_service.handle_connections, daemon=True).start()
    threading.Thread(target=typing_service.handle_forwarding, daemon=True).start()

    # Location Service
    location_service = LocationService()
    threading.Thread(target=location_service.handle_connections, daemon=True).start()
    threading.Thread(target=location_service.handle_forwarding, daemon=True).start()


    # Keep the main thread alive.
    while True:
        pass
    




if __name__ == "__main__":
    main()


