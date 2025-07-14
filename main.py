import threading
from client.chat_feature import ChatFeature
from client.discovery_service import DiscoveryService
from client.document_feature import DocumentFeature
from client.location_feature import LocationFeature
from GUI.chatwindow import ChatWindow
from PyQt5.QtWidgets import QApplication
import sys
import time

from client.translation_feature import TranslationFeature
from client.typing_feature import TypingFeature

if __name__ == "__main__":

    # Discover Servers
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    # typing feature
    typing_feature = TypingFeature()
    threading.Thread(target=typing_feature.handle_connection, args=(server_list,), daemon=True).start()
    threading.Thread(target=typing_feature.handle_listening, daemon=True).start()

    # location feature
    location_feature = LocationFeature()
    threading.Thread(target=location_feature.handle_connection, args=(server_list,), daemon=True).start()
    #threading.Thread(target=live_location.start_location_sharing, daemon=True).start()
    threading.Thread(target=location_feature.handle_listening, daemon=True).start()

    # chat feature
    chat_feature = ChatFeature()
    threading.Thread(target=chat_feature.handle_connection, args=(server_list,), daemon=True).start()

    # translation feature
    translation_feature = TranslationFeature()
    threading.Thread(target=translation_feature.handle_connection, args=(server_list,), daemon=True).start()

    # document feature
    document_feature = DocumentFeature()
    threading.Thread(target=document_feature.handle_connection, args=(server_list,), daemon=True).start()






    time.sleep(1)  # Ensure features are initialized before creating the window
    app = QApplication(sys.argv)
    window = ChatWindow(typing_feature, location_feature, chat_feature, translation_feature, document_feature)  #  Pass both into the window
    window.show()
    sys.exit(app.exec_())
