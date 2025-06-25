import threading
from .discovery_service import DiscoveryService
from .connection_service import ConnectionService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature
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



    # Keep the main thread alive.
    while True:
        pass



    

if __name__ == "__main__":
    main()
