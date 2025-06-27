import threading
from .discovery_service import DiscoveryService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Handle Sending/Receiving of Typing Indicator Feature
    typing_event=TypingFeature()
    threading.Thread(target=typing_event.handle_connection, args=(server_list,), daemon=True).start()
    threading.Thread(target=typing_event.handle_typing, daemon=True).start()
    threading.Thread(target=typing_event.handle_listening, daemon=True).start()

    #Handle Sending/Receiving of Live Location Feature
    live_location=LocationFeature()
    threading.Thread(target=live_location.handle_connection, args=(server_list,), daemon=True).start()
    threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=live_location.handle_listening, daemon=True).start()



    # Keep the main thread alive.
    while True:
        pass



    

if __name__ == "__main__":
    main()
