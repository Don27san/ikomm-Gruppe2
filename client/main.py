# client/main.py

import threading
from .discovery_service import DiscoveryService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature
from .chat_feature import ChatFeature
import time

def run_client_logic():
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
    chat_feature = ChatFeature()
    threading.Thread(target=chat_feature.handle_connection, args=(server_list,), daemon=True).start()

    return typing_event, live_location, chat_feature # for GUI


# main can still be kept for standalone testing of the client logic
def main():
    typing_event, live_location, chat_feature = run_client_logic()
    time.sleep(5)
    chat_feature.send_message("user123", "server456", "Hello from client!")
    while True:
        pass

if __name__ == "__main__":
    main()
