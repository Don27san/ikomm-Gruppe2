# client/main.py

import threading
import time
from .discovery_service import DiscoveryService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature
from .chat import ChatClient

def run_client_logic(user_id="main_client_user"):
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    typing_event = TypingFeature()
    threading.Thread(target=typing_event.handle_connection, args=(server_list,), daemon=True).start()
    threading.Thread(target=typing_event.handle_typing, daemon=True).start()
    threading.Thread(target=typing_event.handle_listening, daemon=True).start()

    # location feature
    live_location = LocationFeature()
    threading.Thread(target=live_location.handle_connection, args=(server_list,), daemon=True).start()
    threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=live_location.handle_listening, daemon=True).start()

    # chat feature
    chat_client = ChatClient(user_id=user_id, server_id="homeserver1")
    # Start chat client connection handling in a separate thread
    threading.Thread(target=chat_client.handle_connection, args=(server_list,), daemon=True).start()

    return typing_event, live_location, chat_client # for GUI


# main can still be kept for standalone testing of the client logic
def main():
    import os
    user_id = os.getenv('CHAT_USER_ID', 'main_client_user')
    recipient_id = os.getenv('CHAT_RECIPIENT_ID', 'other_user')
    
    typing_event, live_location, chat_client = run_client_logic(user_id=user_id)
    
    # Keep the main thread alive and provide a simple chat interface
    try:
        while True:
            if chat_client and chat_client.is_connected:
                message_text = input("Enter message (or type 'quit' to exit): ")
                if message_text.lower() == 'quit':
                    break
                
                recipient_id = input("Enter recipient user ID: ")
                recipient_server = input("Enter recipient server ID: ")

                if message_text and recipient_id and recipient_server:
                    chat_client.send_message_to_user(
                        text_content=message_text,
                        recipient_user_id=recipient_id,
                        recipient_server_id=recipient_server
                    )
                else:
                    print("Message, recipient ID, or recipient server ID cannot be empty.")
            else:
                print("Chat client not connected. Waiting...")
                time.sleep(2)
    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        if chat_client:
            chat_client.close()
        print("Client exited.")

if __name__ == "__main__":
    import time
    main()
