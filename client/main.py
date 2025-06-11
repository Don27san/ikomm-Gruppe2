from . discovery import DiscoveryService
from . connector import ConnectionService


def main():
    #Discovering Servers, Returns list of discovered servers.
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    #Connecting to servers whose features we want to support
    connector = ConnectionService(
        feature_support_list=['TYPING_INDICATOR', 'LIVE_LOCATION'], 
        server_list=server_list)
    connector.connect_client()



if __name__ == "__main__":
    main()
