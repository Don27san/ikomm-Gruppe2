import QtQuick
import QtQuick.Controls

Item {
    id: messageDelegate
    
    // ListView delegate properties
    width: ListView.view ? ListView.view.width : 400
    height: chatMessageRow.height + (isGroupedMessage ? 8 : 32)
    
    // Message properties - can be bound from model or set directly
    property bool isOwnMessage: model ? (model.isOwn || false) : false
    property string userInitials: model ? (model.userInitials || "U") : "U"
    property string avatarColor: model ? (model.avatarColor || "#afdeff") : "#afdeff"
    
    // Message content properties
    property string messageType: model ? (model.messageType || "text") : "text"
    property string messageText: model ? (model.messageText || "") : ""
    property string userId: model ? (model.userId || "") : ""
    property string fileName: model ? (model.fileName || "") : ""
    property string fileSize: model ? (model.fileSize || "") : ""
    property string locationCoord: model ? (model.locationCoord || "") : ""
    property string latitude: model ? (model.latitude || "") : ""
    property string longitude: model ? (model.longitude || "") : ""
    property bool isGroupedMessage: model ? (model.isGroupedMessage || false) : false
    
    property int maxMessageWidth: 400
    
    Row {
        id: chatMessageRow
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: isGroupedMessage ? 8 : 32
        
        layoutDirection: isOwnMessage ? Qt.RightToLeft : Qt.LeftToRight
        spacing: 4
        
        UserAvatar {
            userInitials: messageDelegate.userInitials
            avatarColor: messageDelegate.avatarColor
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            opacity: messageDelegate.isGroupedMessage ? 0.0 : 1.0
        }
        
        Column {
            spacing: 6
            
            // Dynamic message content based on type
            Loader {
                id: messageLoader
                sourceComponent: {
                    switch(messageDelegate.messageType) {
                        case "textContent":
                            return textMessageComponent
                        case "liveLocation":
                            return locationMessageComponent
                        case "document":
                            return documentMessageComponent
                        case "typing":
                            return typingIndicatorComponent
                        default:
                            return textMessageComponent
                    }
                }
            }
        }
    }
    
    // Message type components
    Component {
        id: textMessageComponent
        MessageBubble {
            messageText: messageDelegate.messageText
            isOwnMessage: messageDelegate.isOwnMessage
            maxWidth: messageDelegate.maxMessageWidth
        }
    }
    
    Component {
        id: locationMessageComponent
        LocationMessage {
            userId: messageDelegate.userId
            isOwnMessage: messageDelegate.isOwnMessage
            latitude: messageDelegate.latitude
            longitude: messageDelegate.longitude
            anchors.right: messageDelegate.isOwnMessage ? parent.right : undefined
        }
    }
    
    Component {
        id: documentMessageComponent
        DocumentMessage {
            fileName: messageDelegate.fileName || "Document"
            fileSize: messageDelegate.fileSize || "0 KB"
            anchors.right: messageDelegate.isOwnMessage ? parent.right : undefined
        }
    }
    
    Component {
        id: typingIndicatorComponent
        TypingIndicator {}
    }
}