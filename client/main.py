import threading
from . discovery import DiscoveryService
from . connector import ConnectionService
from .typing_events.send_typing_event import TypingEvent
from .typing_events.receive_typing_events import TypingReceiver


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION'], 
        server_list=server_list)
    connector.connect_client()

    #Handle and send typing events
    typing_event=TypingEvent('localhost', 7778, debounce_time=1)
    threading.Thread(target=typing_event.activate, daemon=True).start()
    
    #Receive typing events
    receive_typing_event = TypingReceiver('localhost', 1234)
    threading.Thread(target=receive_typing_event.listen_for_typing_events, daemon=True).start()





    # Keep the main thread alive.
    while True:
        pass



    

if __name__ == "__main__":
    main()
