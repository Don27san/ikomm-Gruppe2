from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class LocationViewer(QMainWindow):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("共享位置")
        self.setGeometry(100, 100, 800, 600)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
