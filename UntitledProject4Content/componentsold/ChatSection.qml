import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: chatSection
    width: 500; color: "#ffffff"

    property var chatBackend
    ListModel { id: chatModel }  // fill with { type: "text"/"location"/"document", content, outgoing }

    function loadChat(userId) {
        chatModel.clear()
        chatBackend.loadHistory(userId)  // your own API to populate chatModel
    }

    ColumnLayout {
        anchors.fill: parent; spacing: 0

        Frame {
            id: navBar; Layout.fillWidth: true; height: 66
            RowLayout {
                anchors.fill: parent; spacing: 14; Layout.margins: 0
                Image { source: "images/group.png"; width: 37; height: 37; anchors.verticalCenter: parent.verticalCenter }
                Text {
                    text: qsTr("Chat with %1").arg(chatBackend.currentUserId)
                    font.pixelSize: 16; font.styleName: "Semibold"
                    anchors.verticalCenter: parent.verticalCenter
                }
                Item { Layout.fillWidth: true }
                Image { source: "images/tum.png"; width: 49; height: 23; anchors.verticalCenter: parent.verticalCenter }
            }
        }

        MessagesView {
            id: messagesView
            Layout.fillWidth: true; Layout.fillHeight: true
            model: chatModel
        }

        ChatInputBar {
            Layout.fillWidth: true
            backend: chatBackend
        }
    }
}
