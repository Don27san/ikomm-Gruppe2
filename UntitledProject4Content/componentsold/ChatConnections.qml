import QtQuick 2.15

Item {
    property var chatModel
    property var chatListView
    property var chatBackend

    Connections {
        target: chatBackend
        function onMessageReceived(message, author, timestamp) {
            chatModel.append({
                "message": message,
                "author": author,
                "timestamp": timestamp
            })
            if (chatListView) chatListView.positionViewAtEnd()
        }
    }
}
