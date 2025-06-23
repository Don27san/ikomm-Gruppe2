from PyQt5.QtWidgets import QApplication
from chatwindow import ChatWindow
from config2 import config

import sys

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = ChatWindow(config)
        window.show()
        sys.exit(app.exec_())

    except Exception as e:
        import traceback
        print(" Unhandled exception occurred:")
        traceback.print_exc()
        sys.exit(1)
