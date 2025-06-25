import threading
from .announcement_service import AnnouncementService
from .typing_service import TypingService
from .location_service import LocationService


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
    announcer = AnnouncingService(src_addr='localhost', # This is the address it binds to for sending, not necessarily for listening to broadcast
                                src_port=9999, # Port for discovery protocol
                                server_id=main_server_id, 
                                features=server_features)
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
    try:
        while True:
            pass # Main thread keeps other daemon threads alive
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Add cleanup for other services if necessary
        print("Server exited.")


if __name__ == "__main__":
    main()


