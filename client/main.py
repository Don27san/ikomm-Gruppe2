# client/main.py

import sys
import threading
from PyQt5.QtWidgets import QApplication
from GUI.chatwindow import ChatWindow  # Adjust import as needed

from .discovery_service import DiscoveryService
from .typing_feature import TypingFeature
from .location_feature import LocationFeature

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
    #threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=live_location.handle_listening, daemon=True).start()

    return typing_event, live_location # for GUI
#
#
# # main can still be kept for standalone testing of the client logic
# def main():
#     run_client_logic()
#     while True:
#         pass  # Keep the threads alive (for debugging only)
#
# if __name__ == "__main__":
#     main()

# Keep window reference alive
window = None

def main():
    global window
    app = QApplication(sys.argv)
    typing_feature, location_feature = run_client_logic()
    window = ChatWindow(typing_feature, location_feature)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
