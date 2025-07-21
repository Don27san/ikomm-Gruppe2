import QtQuick
import QtQuick.Controls

ListView {
    id: listView
    anchors.fill: parent
    model: model
    spacing: 32
    clip: true

    delegate: Loader {
        width: parent.width
        property var msg: model  // contains type, content, outgoing

        sourceComponent: {
            switch (msg.type) {
                case "location": return Qt.createComponent("LocationMessageDelegate.qml")
                case "document": return Qt.createComponent("DocumentMessageDelegate.qml")
                default: return Qt.createComponent("TextMessageDelegate.qml")
            }
        }

        onLoaded: {
            item.content = msg.content
            item.outgoing = msg.outgoing
        }
    }
}
