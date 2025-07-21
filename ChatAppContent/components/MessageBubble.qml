import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    
    property string messageText: ""
    property bool isOwnMessage: false
    property int maxWidth: 400
    
    color: isOwnMessage ? "#1f5cf1" : "#eeeeee"
    radius: 16
    anchors.right: isOwnMessage ? parent.right : undefined
    anchors.rightMargin: isOwnMessage ? 0 : undefined
    
    width: Math.min(messageText.length > 0 ? 
                   textContent.implicitWidth + 24 : 60, maxWidth)
    height: textContent.paintedHeight + 24

    Text {
        id: textContent
        anchors.fill: parent
        anchors.margins: 12
        text: messageText
        font.pixelSize: 14
        color: isOwnMessage ? "#ffffff" : "#000000"
        wrapMode: Text.WrapAnywhere
        width: parent.width - 24
    }
}