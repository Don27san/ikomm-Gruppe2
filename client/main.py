import threading
from .discovery_service import DiscoveryService
from .connection_service import ConnectionService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION'], 
        server_list=server_list)
    connector.connect_client()

    #Handle Sending/Receiving of Typing Indicator Feature
    typing_event=TypingFeature()
    threading.Thread(target=typing_event.handle_typing, daemon=True).start()
    threading.Thread(target=typing_event.handle_listening, daemon=True).start()

    #Handle Sending/Receiving of Live Location Feature
    live_location=LocationFeature()
    threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=live_location.handle_listening, daemon=True).start()



    # Keep the main thread alive.
    while True:
        pass



    

if __name__ == "__main__":
    main()
