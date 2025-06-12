import threading
from .announcer import AnnouncingService
from .typing_service import TypingService
from .chat_server import start_server as start_chat_server, SERVER_ID as CHAT_SERVER_ID, PORT as CHAT_PORT


def main():
    # Define server features
    main_server_id = CHAT_SERVER_ID # Aligning main server ID with chat server's ID for simplicity

    server_features = [
        {'name': 'TYPING_INDICATOR', 'port': 7777}, # Assuming this is the port for typing subscription
        {'name': 'CHAT', 'port': CHAT_PORT} # Use the port from chat_server
    ]

    # Listen for discovery calls and announce server
    announcer = AnnouncingService(src_addr='localhost', src_port=9999, server_id=main_server_id, features=server_features)
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Start Chat Service
    threading.Thread(target=start_chat_server, daemon=True).start()

    # Typing Indicator Feature
    typing_service = TypingService()
    threading.Thread(target=typing_service.handle_connections, daemon=True).start()
    threading.Thread(target=typing_service.handle_forwarding, daemon=True).start()
    
    print("Server started with all services running...")
    print(f"Chat Service: TCP port {CHAT_PORT}")
    print("Discovery Service: UDP port 9999")
    print("Typing Service: Check typing_service configuration")

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


