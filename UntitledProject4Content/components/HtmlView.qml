import QtQuick
import QtWebEngine
import QtQuick.Controls



WebEngineView {
        id: webView
        anchors.fill: parent
        url: Qt.resolvedUrl("map.html")

        settings.localContentCanAccessRemoteUrls: true
        settings.localContentCanAccessFileUrls: true

        onLoadingChanged: function(loadRequest) {
            if (loadRequest.status === WebEngineView.LoadSuccessStatus) {
                console.log("HTML loaded successfully")
            } else if (loadRequest.status === WebEngineView.LoadFailedStatus) {
                console.log("Load failed:", loadRequest.errorString)
            }
        }
    }

