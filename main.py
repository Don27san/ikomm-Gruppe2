from client.main import run_client_logic
from GUI.chatwindow import ChatWindow
from PyQt5.QtWidgets import QApplication
import sys
import time

if __name__ == "__main__":
    typing_feature, location_feature, chat_feature = run_client_logic()  #  Receive both instances

    time.sleep(1)  #  doesn't work without this delay, probably due to threading issues
    
    app = QApplication(sys.argv)
    window = ChatWindow(typing_feature, location_feature)  #  Pass both into the window
    window.show()
    sys.exit(app.exec_())
