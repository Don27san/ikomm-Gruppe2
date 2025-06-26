import sys
from PyQt5.QtWidgets import QApplication
from chatwindow import ChatWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
