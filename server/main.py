import threading
from . announcer import AnnouncingService
from . typing_subscriber import TypingSubscriber
from . typing_forwarder import TypingForwarder
from .chat_server import start_server as start_chat_server, SERVER_ID as CHAT_SERVER_ID, PORT as CHAT_PORT


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

    # Listen for client connections w.r.t. typing indicator feature
    # The TypingSubscriber might also need to be aware of the main_server_id if it registers clients against it
    typing_subscriber = TypingSubscriber(src_addr='localhost', src_port=7777) # Port where typing subscription happens
    threading.Thread(target=typing_subscriber.listen_for_subscription_requests, daemon=True).start()

    #Listen for and forward incoming typing_events
    # The TypingForwarder might also need context about server IDs if it interacts with other servers
    typing_forwarder = TypingForwarder('localhost', 7778) # Port where typing events are received by server to be forwarded
    threading.Thread(target=typing_forwarder.handle_forwarding, daemon=True).start()
    
    # Start the Chat Server
    print(f"Starting Chat Server (ID: {CHAT_SERVER_ID}) on port {CHAT_PORT}...")
    threading.Thread(target=start_chat_server, daemon=True).start()

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


