import QtQuick
import QtQuick.Window
import QtWebEngine
import QtQuick.Controls

ApplicationWindow {
    id: locationWindow
    width: 800
    height: 600
    title: "Live Location"
    visible: false
    
    property real latitude: 0.0
    property real longitude: 0.0
    property string authorName: ""
    
    // Function to show the window (equivalent to show() in PyQt5)
    function showWindow() {
        visible = true
        raise()
        requestActivate()
    }
    
    // Function to update location (equivalent to updateLocation in PyQt5)
    function updateLocation(lat, lon, author) {
        latitude = lat
        longitude = lon
        authorName = author
        
        // Update the web view with new coordinates
        var htmlPath = Qt.resolvedUrl("map.html")
        var urlWithParams = htmlPath + "?lat=" + lat + "&lon=" + lon + "&author=" + encodeURIComponent(author)
        webView.url = urlWithParams
        
        // Alternative: Call JavaScript directly if map is already loaded
        // webView.runJavaScript("updatePosition(" + lat + ", " + lon + ", '" + author + "');")
    }
    
    WebEngineView {
        id: webView
        anchors.fill: parent
        
        settings.localContentCanAccessRemoteUrls: true
        settings.localContentCanAccessFileUrls: true
        settings.allowRunningInsecureContent: true
        
        onLoadingChanged: {
            if (loadRequest.status === WebEngineView.LoadSucceededStatus) {
                console.log("Map loaded successfully")
                // If you want to call updatePosition after initial load
                if (latitude !== 0.0 && longitude !== 0.0) {
                    var js = "updatePosition(" + latitude + ", " + longitude + ", '" + authorName + "');"
                    runJavaScript(js)
                }
            } else if (loadRequest.status === WebEngineView.LoadFailedStatus) {
                console.log("Failed to load map:", loadRequest.errorString)
            }
        }
        
        // Handle JavaScript calls if needed
        onJavaScriptConsoleMessage: {
            console.log("JS Console:", message)
        }
    }
    
    // Optional: Add a toolbar or status bar
    header: ToolBar {
        visible: authorName !== ""
        
        Row {
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            spacing: 10
            
            Text {
                text: "Tracking: " + authorName
                font.pixelSize: 14
                color: "#333"
            }
            
            Text {
                text: "Location: " + latitude.toFixed(6) + ", " + longitude.toFixed(6)
                font.pixelSize: 12
                color: "#666"
            }
        }
        
        Row {
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            
            Button {
                text: "Close"
                onClicked: locationWindow.visible = false
            }
        }
    }
}