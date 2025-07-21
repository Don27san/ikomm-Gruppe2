import QtQuick
import QtQuick.Controls

Rectangle {
    property alias content: messageItem.text
    property bool outgoing: false

    color: outgoing ? "#1f5cf1" : "#eeeeee"
    radius: 16

    width: Math.min(messageItem.implicitWidth + 24, 400)
    height: messageItem.paintedHeight + 24

    Text {
        id: messageItem
        wrapMode: Text.WordWrap
        anchors.fill: parent; anchors.margins: 12
        font.pixelSize: 14
        color: outgoing ? "#ffffff" : "#000000"
        width: parent.width - 24
    }
}
