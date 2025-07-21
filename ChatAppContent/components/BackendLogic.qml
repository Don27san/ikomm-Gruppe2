import QtQuick

QtObject {
    id: backendLogic
    property Item ui                // will be set to your ChatInputBar root
    property var chatBackend        // injected from UI

    Connections {
        target: chatBackend
        function onContactClicked(contactId) {
            console.log("Contact selected:", contactId)
            // Backend should filter and populate the filteredChatModel
            
            filterMessagesForContact(contactId)
        }
    }

    Connections {
        target: chatBackend
        function onMessageReceived(contactId, isOwn, userInitials, avatarColor, messageType, messageText, userId, isGroupedMessage) {
            console.log("New message received for:", contactId)
            
            // Add to filteredChatModel if it's for the currently selected contact
            if (ui.selectedContactId === contactId) {
                ui.filteredChatModel.append({
                    isOwn: isOwn,
                    userInitials: userInitials,
                    avatarColor: avatarColor,
                    messageType: messageType,
                    messageText: messageText,
                    userId: userId,
                    isGroupedMessage: isGroupedMessage
                })
            }
        }
    }


    function filterMessagesForContact(contactId) {
        // Clear the filtered model
        ui.filteredChatModel.clear()
        
        // Ask backend to provide filtered messages for this contact
        // Backend should call populateFilteredMessages with the filtered data
        chatBackend.getMessagesForContact(contactId)
    }

    Connections {
        target: chatBackend
        function onPopulateFilteredMessages(messages) {
            ui.filteredChatModel.clear()
            
            for (var i = 0; i < messages.length; i++) {
                var msg = messages[i]
                ui.filteredChatModel.append({
                    isOwn: msg.isOwn || false,
                    userInitials: msg.userInitials || "",
                    avatarColor: msg.avatarColor || "",
                    messageType: msg.messageType || "text",
                    messageText: msg.messageText || "",
                    userId: msg.userId || "",
                    isGroupedMessage: msg.isGroupedMessage || false
                })
            }
        }
    }

    }
}