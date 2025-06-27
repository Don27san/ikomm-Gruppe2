import threading
from .announcement_service import AnnouncementService
from .typing_service import TypingService
from .location_service import LocationService
from .chat_server import start_server as start_chat_server


def main():
    # Listen for discovery calls and announce server
    announcer = AnnouncementService()
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Chat Service (main messaging functionality)
    threading.Thread(target=start_chat_server, daemon=True).start()

    # Typing Indicator Feature
    typing_service = TypingService()
    threading.Thread(target=typing_service.handle_connections, daemon=True).start()
    threading.Thread(target=typing_service.handle_forwarding, daemon=True).start()

    # Location Service
    location_service = LocationService()
    threading.Thread(target=location_service.handle_connections, daemon=True).start()
    threading.Thread(target=location_service.handle_forwarding, daemon=True).start()

    print("Server started with all services running...")
    print("Chat Service: TCP port 6001")
    print("Discovery Service: UDP port 9999")
    print("Typing Service: Check typing_service configuration")
    print("Location Service: Check location_service configuration")

    # Keep the main thread alive.
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down server...")


if __name__ == "__main__":
    main()


