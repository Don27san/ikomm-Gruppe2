import threading
from . discovery import DiscoveryService
from . connector import ConnectionService
from . typing_event import TypingEvent


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION'], 
        server_list=server_list)
    connector.connect_client()

    #Handle typing events
    typing_event=TypingEvent('localhost', 7778, debounce_time=1)
    typing_event.activate()

    

if __name__ == "__main__":
    main()
