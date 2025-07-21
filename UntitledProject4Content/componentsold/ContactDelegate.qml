import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    id: root
    property string userId
    property string serverId
    height: 52; flat: true

    RowLayout {
        anchors.fill: parent; spacing: 10; Layout.margins: 10

        Rectangle {
            width: 34; height: 34; radius: 17; color: "#afdeff"
            Text {
                text: userId.charAt(0)
                anchors.centerIn: parent
                font.pixelSize: 13; font.styleName: "Bold"; color: "#9c000000"
            }
        }

        Text {
            text: userId + "@" + serverId
            font.pixelSize: 15; font.styleName: "Semibold"
            verticalAlignment: Text.AlignVCenter
        }
    }
}
