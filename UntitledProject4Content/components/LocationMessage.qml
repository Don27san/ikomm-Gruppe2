import QtQuick
import QtQuick.Controls

Rectangle {
    id: locationRoot
    
    property string userId: ""
    property bool isOwnMessage: false
    property real latitude: 0
    property real longitude: 0
    
    width: 250
    height: 105
    color: "#eeeeee"
    radius: 16
    
    Column {
        anchors.fill: parent
        spacing: 8
        padding: 12

        Row {
            spacing: 8

            Rectangle {
                width: 40
                height: 40
                color: "#1f5cf1"
                radius: 500

                Image {
                    width: 15
                    source: "../images/location_icon.png"
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                }
            }

            Column {
                width: 130
                spacing: 4

                Text {
                    text: qsTr("Live Location")
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                }

                Text {
                    width: 175
                    color: "#575757"
                    text: userId + " started sharing"
                    font.pixelSize: 12
                    wrapMode: Text.WrapAnywhere
                }
            }
        }

        Button {
            height: 35
            text: ""
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            flat: true
            
            Rectangle {
                color: "#fafafa"
                radius: 10
                anchors.fill: parent
            }

            Text {
                text: qsTr("View Location")
                font.pixelSize: 12
                font.styleName: "Semibold"
                anchors.centerIn: parent
            }

            onClicked: {
                function findByName(parent, name) {
                    if (parent.objectName === name) return parent;
                    for (var i = 0; i < parent.children.length; i++) {
                        var result = findByName(parent.children[i], name);
                        if (result) return result;
                    }
                    return null;
                }
                
                var root = locationRoot;
                while (root.parent) root = root.parent;
                
                var mainWindow = findByName(root, "mainWindow");
                if (mainWindow && mainWindow.webView) {
                    var fileUrl = Qt.resolvedUrl("../map.html") + "?lat=" + latitude + "&lon=" + longitude + "&author=" + encodeURIComponent(userId)
                    mainWindow.webView.url = fileUrl;
                    mainWindow.showHtmlOverlay = true;
                }
            }
        }
    }

}