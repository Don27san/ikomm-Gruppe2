import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    property alias message: messageText.text
    property bool outgoing: false

    // size itself to the text
    implicitWidth: messageText.implicitWidth + 24
    implicitHeight: messageText.implicitHeight + 16

    Rectangle {
        id: bubble
        anchors.top: parent.top
        anchors.topMargin: 4
        anchors.right: outgoing ? parent.right : undefined
        anchors.left: !outgoing ? parent.left : undefined
        anchors.horizontalCenter: outgoing ? undefined : parent.horizontalCenter
        anchors.rightMargin: outgoing ? 8 : 0
        anchors.leftMargin: !outgoing ? 8 : 0
        implicitWidth: messageText.implicitWidth + 24
        implicitHeight: messageText.implicitHeight + 16
        radius: 8
        color: outgoing ? "#CFE9FF" : "#EEEEEE"

        Text {
            id: messageText
            anchors.fill: parent
            anchors.margins: 8
            wrapMode: Text.Wrap
            font.pixelSize: 14
        }
    }
}