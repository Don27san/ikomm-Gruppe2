import threading
import time
from .discovery_service import DiscoveryService
from .connection_service import ConnectionService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature
from .chat import ChatClient
from config import config


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=config['feature_support'], 
        server_list=server_list)
    connected_servers = connector.connect_client() # Assuming this returns info about connected servers

    #Handle Sending/Receiving of Typing Indicator Feature
    typing_event=TypingFeature()
    threading.Thread(target=typing_event.handle_typing, daemon=True).start()
    threading.Thread(target=typing_event.handle_listening, daemon=True).start()

    #Handle Sending/Receiving of Live Location Feature
    live_location=LocationFeature()
    threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=live_location.handle_listening, daemon=True).start()

    # Initialize Chat Client
    my_user_id = "user_main_client" 
    my_homeserver_id = "homeserver1"

    chat_client = None
    chat_server_host = 'localhost'
    chat_server_port = config['chat_feature']['server_port']
    
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

                if message_text and recipient_id and recipient_server:
                    chat_client.send_message_to_user(
                        text_content=message_text,
                        recipient_user_id=recipient_id,
                        recipient_server_id=recipient_server
                    )
                else:
                    print("Message, recipient ID, or recipient server ID cannot be empty.")
            else:
                print("Chat client not connected. Retrying or waiting...")
                time.sleep(5)
                if not chat_client or not chat_client.is_connected:
                    chat_client = ChatClient(user_id=my_user_id, server_id=my_homeserver_id,
                                             server_host=chat_server_host, server_port=chat_server_port)

    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        if chat_client:
            chat_client.close()
        print("Client exited.")


if __name__ == "__main__":
    main()
