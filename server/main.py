import threading
from .announcer import AnnouncingService
from .typing_service import TypingService
from .location_service import LocationService
from .chat_server import start_server as start_chat_server


def main():
    # Define server features
    # The SERVER_ID for chat_server is defined in chat_server.py, we use it here for consistency
    # Or, you could define a global server ID here and pass it to all services.
    # For now, let's assume chat_server.py's SERVER_ID is the main one for chat.
    # The AnnouncingService needs its own server_id for the announcement message itself.
    # Let's use a general server ID for the announcer and specific ports for features.
    main_server_id = CHAT_SERVER_ID # Aligning main server ID with chat server's ID for simplicity

    server_features = [
        {'name': 'TYPING_INDICATOR', 'port': 7777}, # Assuming this is the port for typing subscription
        {'name': 'CHAT', 'port': CHAT_PORT} # Use the port from chat_server
    ]

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


