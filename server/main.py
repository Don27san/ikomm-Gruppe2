import threading
from .announcement_service import AnnouncementService
from .typing_service import TypingService


def main():
    # Listen for discovery calls and announce server
    announcer = AnnouncementService()
    threading.Thread(target=announcer.announce_server, daemon=True).start()

    # Typing Indicator Feature
    typing_service= TypingService()
    threading.Thread(target=typing_service.handle_connections, daemon=True).start()
    threading.Thread(target=typing_service.handle_forwarding, daemon=True).start()
    

    # Keep the main thread alive.
    while True:
        pass
    




if __name__ == "__main__":
    main()


