import threading
import time # Added import for time.sleep
from . discovery import DiscoveryService
from . connector import ConnectionService
from .typing_events.send_typing_event import TypingEvent
from .typing_events.receive_typing_events import TypingReceiver
from .chat import ChatClient # Added import


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION', 'CHAT'], # Added CHAT
        server_list=server_list)
    connected_servers = connector.connect_client() # Assuming this returns info about connected servers

    #Handle and send typing events
    typing_event=TypingEvent('localhost', 7778, debounce_time=1)
    threading.Thread(target=typing_event.activate, daemon=True).start()
    
    #Receive typing events
    receive_typing_event = TypingReceiver('localhost', 1234)
    threading.Thread(target=receive_typing_event.listen_for_typing_events, daemon=True).start()

    # Initialize Chat Client
    # Placeholder: Determine user_id and homeserver_id (e.g., from config or user input)
    my_user_id = "user_main_client" 
    my_homeserver_id = "homeserver1" # This should ideally be determined dynamically or from config

    chat_client = None
    # Attempt to connect to a server that supports CHAT
    # This logic might need refinement based on how ConnectionService and server_list work
    chat_server_host = 'localhost' # Default
    chat_server_port = 5001 # Default from chat.py
    
    # Example: Find a server that announced CHAT feature (if your discovery/connector supports this)
    # Or, connect to a known chat server. For now, using defaults.
    # if connected_servers and 'CHAT' in connected_servers:
    #     chat_server_host = connected_servers['CHAT']['host'] 
    #     chat_server_port = connected_servers['CHAT']['port']

    print(f"Attempting to connect to chat server at {chat_server_host}:{chat_server_port}")
    chat_client = ChatClient(user_id=my_user_id, server_id=my_homeserver_id, 
                             server_host=chat_server_host, server_port=chat_server_port)

    # Keep the main thread alive and provide a simple chat interface.
    try:
        while True:
            if chat_client and chat_client.is_connected:
                message_text = input("Enter message (or type 'quit' to exit chat): ")
                if message_text.lower() == 'quit':
                    break
                
                recipient_id = input("Enter recipient user ID: ")
                recipient_server = input("Enter recipient user's server ID: ")
                # For group messages, you would add similar inputs

                if message_text and recipient_id and recipient_server:
                    chat_client.send_chat_message(
                        text_content=message_text,
                        recipient_user_id=recipient_id,
                        recipient_server_id=recipient_server
                    )
                else:
                    print("Message, recipient ID, or recipient server ID cannot be empty.")
            else:
                # Basic wait if chat client is not yet connected or failed
                print("Chat client not connected. Retrying or waiting...")
                time.sleep(5) # Wait before prompting again or retrying connection
                # Potentially re-initialize or attempt re-connect if chat_client is None or not connected
                if not chat_client or not chat_client.is_connected:
                    chat_client = ChatClient(user_id=my_user_id, server_id=my_homeserver_id,
                                             server_host=chat_server_host, server_port=chat_server_port)


    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        if chat_client:
            chat_client.close()
        # Add cleanup for other services if necessary
        print("Client exited.")

    # Keep the main thread alive.
    while True:
        pass



    

if __name__ == "__main__":
    main()
