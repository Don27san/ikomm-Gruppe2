from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class LocationViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Live Location")
        self.setGeometry(100, 100, 800, 600)
        self.browser = QWebEngineView()
        # allow local HTML to fetch remote CDN assets
        from PyQt5.QtWebEngineWidgets import QWebEngineSettings
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        # load local Leaflet map HTML
        import os
        html = os.path.join(os.path.dirname(__file__), "map.html")
        self.browser.load(QUrl.fromLocalFile(html))
        self.setCentralWidget(self.browser)

    def updateLocation(self, lat, lon):
        # call JS to move marker without full reload
        js = f"updatePosition({lat}, {lon});"
        self.browser.page().runJavaScript(js)
