import threading
from . announcer import AnnouncingService
from . typing_subscriber import TypingSubscriber


def main():
    # Listen for discovery calls and announce server
    announcer = AnnouncingService(src_addr='localhost', src_port=9999)
    # Listen for client connections w.r.t. typing indicator feature
    typing_subscriber = TypingSubscriber(src_addr='localhost', src_port=7777)






    # Start both loops in separate threads
    threading.Thread(target=typing_subscriber.listen_for_subscription_requests, daemon=True).start()
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Keep the main thread alive (or do other work)
    while True:
        pass
    




if __name__ == "__main__":
    main()


