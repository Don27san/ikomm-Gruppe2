
import QtQuick
import QtQuick.Controls
import "."

Item {
    id: messageDelegate
    
    width: ListView.view ? ListView.view.width : 400
    height: chatMessage.height + (model.isGroupedMessage ? 8 : 32)
    
    ChatMessage {
        id: chatMessage
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: model.isGroupedMessage ? 8 : 32
        
        isOwnMessage: model.isOwn || false
        userInitials: model.userInitials || "U"
        avatarColor: model.avatarColor || "#afdeff"
        
        messageType: model.messageType || "text"
        messageText: model.messageText || ""
        userId: model.userId || ""
        fileName: model.fileName || ""
        fileSize: model.fileSize || ""
        isGroupedMessage: model.isGroupedMessage || false
        maxMessageWidth: 400
    }
}