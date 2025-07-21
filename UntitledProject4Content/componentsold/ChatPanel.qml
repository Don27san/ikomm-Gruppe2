import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    property var chatModel
    property var chatBackend

    function loadChat(contactId) {
        chatBackend.loadHistory(contactId)
    }

    ColumnLayout {
        anchors.fill: parent; spacing: 0

        ChatHeader { title: root.chatBackend.currentChatTitle }

        MessagesView {
            id: messagesView
            model: root.chatModel
            Layout.fillWidth: true; Layout.fillHeight: true
        }

        ChatInputBar {
            Layout.fillWidth: true
            backend: root.chatBackend
            onSendMessage: backend.sendMessage(text)
        }
    }
}