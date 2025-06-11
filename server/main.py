import threading
from . announcer import AnnouncingService
from . typing_subscriber import TypingSubscriber
from . typing_forwarder import TypingForwarder


def main():
    # Listen for discovery calls and announce server
    announcer = AnnouncingService(src_addr='localhost', src_port=9999)
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Listen for client connections w.r.t. typing indicator feature
    typing_subscriber = TypingSubscriber(src_addr='localhost', src_port=7777)
    threading.Thread(target=typing_subscriber.listen_for_subscription_requests, daemon=True).start()

    #Listen for and forward incoming typing_events
    typing_forwarder = TypingForwarder('localhost', 7778)
    threading.Thread(target=typing_forwarder.handle_forwarding, daemon=True).start()
    

    # Keep the main thread alive.
    while True:
        pass
    




if __name__ == "__main__":
    main()


