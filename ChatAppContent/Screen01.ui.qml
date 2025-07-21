
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import ChatApp
import QtQuick.Timeline 1.0
import QtQml.Models
import "components"
import QtWebEngine


Rectangle {
    id: rectangle
    objectName: "mainWindow"
    width: 750
    height: 700
    color: "#ffffff"
    property string selectedContactId: ""

    property bool showHtmlOverlay: false
    property bool showAddContact: false
    property alias webView: webView

    property string myContactId: chatBackend.myContactId

    Rectangle {
        id: addContactOverlay
        visible: showAddContact
        anchors.fill: parent
        color: "#80000000"
        z: 999
        MouseArea {
            anchors.fill: parent
            onClicked: showAddContact = false
        }
    }

    // Centered AddContact loader, on top of overlay
    Loader {
        id: addContactLoader
        active: showAddContact
        source: showAddContact ? "components/AddContact.qml" : ""
        anchors.centerIn: parent // center in the window
        z: 1001 // above the overlay
        visible: showAddContact
    }
    
    Rectangle {
        id: htmlOverlay
        visible: showHtmlOverlay
        anchors.fill: parent
        color: "#80000000"
        z: 1000
        MouseArea { anchors.fill: parent; onClicked: showHtmlOverlay = false}
    }

    WebEngineView {
        id: webView
        visible: showHtmlOverlay
        enabled: showHtmlOverlay
        anchors.centerIn: parent
        width: 500
        height: 500
        url: Qt.resolvedUrl("map.html")
        z: 1002
        settings.localContentCanAccessRemoteUrls: true
        settings.localContentCanAccessFileUrls: true
    }

    Connections {
        target: chatBackend
        function onLocationReceived(lat, lon, author) {
            if (showHtmlOverlay) {
                webView.runJavaScript("updatePosition(" + lat + ", " + lon + ", '" + author + "');")
            }
        }
    }

    ListModel {
        id: contactsModel
    }

    // This model will be populated by the backend based on selected contact
    ListModel {
        id: chatModel
    }

    Connections {
        target: chatBackend
        function onMessageReceived(message, messageType, author, userInitials, avatarColor, isOwn) {
            // Ignore if no contact selected
            if (rectangle.selectedContactId === "")
                return
            if (author !== rectangle.selectedContactId) 
                return
            // Only append message if it's from the selected contact
            //var fromSelectedContact = (author === rectangle.selectedContactId)
            //var isOwn = !fromSelectedContact
            var existingTypingIndex = -1

            if (messageType === "typing") {
                // Only show typing for the selected contact
                for (var i = 0; i < chatModel.count; i++) {
                    var item = chatModel.get(i)
                    if (item.messageType === "typing" && item.userId === author) {
                        existingTypingIndex = i
                        break
                    }
                    
                }
            }


            var fileName = ""
            var fileSize = ""
            var latitude = ""
            var longitude = ""

            if (messageType === "liveLocation" && message.indexOf(":") !== -1) {
                var parts = message.split(":")
                message = ""
                latitude = parts[0] + ""
                longitude = parts[1] + ""
            } else if (messageType === "document") {
                // If messageText is formatted as 'filename|filesize', split it
                var fileParts = message.split("|")
                fileName = fileParts[0] || "Unknown file"
                fileSize = fileParts[1] || "Unknown size"
            }
            if (existingTypingIndex === -1) {
                onRemoveTypingMessage(author)
                chatModel.append({
                    "isOwn": isOwn,
                    "userInitials": userInitials,
                    "avatarColor": avatarColor,
                    "messageType": messageType,
                    "messageText": message,
                    "fileName": fileName,
                    "fileSize": fileSize,
                    "latitude": latitude,
                    "longitude": longitude,
                    "userId": isOwn ? rectangle.myContactId : author,
                    "isGroupedMessage": false
                })
                chatListView.positionViewAtEnd()
            }
        }

        function onRemoveTypingMessage(author) {
            for (var i = chatModel.count - 1; i >= 0; i--) {
                var item = chatModel.get(i)
                if (item.messageType === "typing" && item.userId === author) {
                    console.log("Removing typing message for:", author)
                    chatModel.remove(i)
                    break // Remove only the first matching typing message
                }
            }
        }
    }

    Row {
        id: application_container
        anchors.fill: parent

        Rectangle {
            id: contact_section
            width: 250
            color: "#ffffff"
            border.color: "#d0d3d7"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: -1
            anchors.topMargin: -1
            anchors.bottomMargin: -1

            Frame {
                id: frame1
                height: 66
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.topMargin: 0
                contentWidth: 690
                background: Rectangle {
                    color: "transparent"
                    border.width: 0
                }

                Text {
                    id: text3
                    y: 11
                    text: qsTr("My Contacts")
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    font.pixelSize: 16
                    font.styleName: "Semibold"
                }

                Button {
                    id: add_contact_button
                    width: 55
                    height: 52
                    text: qsTr("")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    property bool isActive: false
                    y: 312
                    flat: true
                    onClicked: showAddContact = true
                    Rectangle {
                        id: rectangle5
                        color: "#00ffffff"
                        anchors.fill: parent
                    }

                    Image {
                        id: new_contact
                        width: 20
                        source: "images/new_contact.png"
                        anchors.centerIn: parent
                        fillMode: Image.PreserveAspectFit
                    }
                }
            }

            ListView {
                id: contactsListView
                anchors.fill: parent
                anchors.topMargin: 66
                anchors.bottomMargin: 120
                clip: true // Space for demo buttons

                model: contactsModel
                currentIndex: -1

                delegate: ContactItem {
                    contactId: model.contactId
                    userInitials: model.userInitials
                    avatarColor: model.avatarColor
                }

                // Smooth scrolling
                ScrollBar.vertical: ScrollBar {
                    active: true
                    policy: ScrollBar.AsNeeded
                    width: 8
                }

                Connections {
                    target: contactsListView
                    function onCurrentIndexChanged() {
                        if (contactsListView.currentIndex >= 0 && chatBackend) {
                            chatModel.clear()
                            rectangle.selectedContactId = contactsListView.currentItem.contactId
                            // Backend handles filtering and populating chatModel
                            chatBackend.contactClicked(
                                        rectangle.selectedContactId)
                        }
                    }
                }
                Connections {
                    target: chatBackend
                    function onContactAdded(contactId, userInitials, avatarColor) {
                        console.log("Adding contact:", contactId)
                        showAddContact = false
                        contactsModel.append({
                                                 "contactId": contactId,
                                                 "userInitials": userInitials,
                                                 "avatarColor": avatarColor
                                             })
                    }
                }
            }
        }

        Rectangle {
            id: chat_section
            width: 500
            color: "#ffffff"
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.bottomMargin: 0

            Frame {
                id: chat_nav_bar
                height: 66
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.topMargin: 0
                background: Rectangle {
                    color: "transparent"
                    border.width: 0
                }

              //  Image {
            //        id: group
          //          width: 37
        //            height: 37
      //              anchors.verticalCenter: parent.verticalCenter
    //                anchors.left: parent.left
  //                  anchors.leftMargin: 0
//                    source: "images/group.png"
//                    fillMode: Image.PreserveAspectFit
//                }

                Rectangle {
                    id: userIcon
                    width: 37
                    height: 37
                    color: selectedContactId ? contactsListView.currentItem.avatarColor : "#afdeff"
                    radius: 17
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                Image {
                    id: group
                    width: 37
                    height: 37
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    source: "images/group.png"
                    fillMode: Image.PreserveAspectFit
                    visible: !selectedContactId
                }
                    
                    Text {
                        id: userNameAbbreviated
                        color: "#9c000000"
                        text: selectedContactId ? contactsListView.currentItem.userInitials : "U"
                        font.pixelSize: 13
                        font.styleName: "Bold"
                        anchors.centerIn: parent
                        visible: selectedContactId
                    }
                }

                Text {
                    id: text1
                    x: 51
                    y: 11
                    text: selectedContactId ? "Chat with " + selectedContactId : "Select a Contact"
                    font.pixelSize: 16
                    font.styleName: "Semibold"
                }

                Image {
                    id: tum
                    x: 427
                    width: 49
                    height: 23
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    source: "images/tum.png"
                    fillMode: Image.PreserveAspectFit
                }
            }

            Item {
                anchors.fill: parent

                ListView {
                    id: chatListView
                    anchors.fill: parent
                    anchors.topMargin: 66
                    anchors.bottomMargin: chat_controls.height
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    clip: true

                    // Show when contact is selected and messages exist
                    visible: selectedContactId !== "" && chatModel.count > 0

                    // Use the filtered model populated by backend
                    model: chatModel

                    delegate: ChatMessage {}

                    // Smooth scrolling
                    ScrollBar.vertical: ScrollBar {
                        active: true
                        policy: ScrollBar.AsNeeded
                        width: 8
                    }

                    // Add some spacing at the top and bottom
                    header: Item {
                        height: 20
                    }
                    footer: Item {
                        height: 20
                    }

                    // Enable flicking for smooth scrolling
                    flickableDirection: Flickable.VerticalFlick
                }

                Text {
                    text: qsTr("📨 Select a contact to start chatting")
                    anchors.centerIn: parent
                    color: "#888"
                    font.pixelSize: 16
                    visible: selectedContactId === ""
                    z: 1
                }

                Text {
                    text: qsTr("📝 Send a message to this user")
                    anchors.centerIn: parent
                    color: "#888"
                    font.pixelSize: 16
                    visible: selectedContactId !== "" && chatModel.count === 0
                    z: 1
                }
            }

            Rectangle {
                id: chat_controls
                height: row3.implicitHeight
                color: "#ffffff"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.bottomMargin: 0

                Row {
                    id: row3
                    anchors.fill: parent
                    spacing: 4
                    padding: 10

                    ComboBox {
                        id: comboBox
                        width: 50
                        height: input_comp.height
                        clip: true
                        textRole: "text"
                        valueRole: "code"
                        opacity: rectangle.selectedContactId.length > 0 ? 1.0 : 0.5
                        enabled: rectangle.selectedContactId.length > 0
                        indicator: Item {}

                        model: ListModel {
                            ListElement {
                                text: ""
                                code: ""
                            } // ⬅️ Default item, triggers icon
                            ListElement {
                                text: "🇩🇪"
                                code: "DE"
                            }
                            ListElement {
                                text: "🇨🇳"
                                code: "ZH"
                            }
                            ListElement {
                                text: "🇬🇧"
                                code: "EN"
                            }
                            ListElement {
                                text: "🇹🇷"
                                code: "TR"
                            }
                        }

                        onActivated: comboBox.focus = false

                        background: Rectangle {
                            color: "white"
                            radius: 6
                            border.width: 2
                            border.color: (comboBox.focus
                                           || comboBox.popup.visible) ? "#1f5cf1" : "transparent"
                        }

                        popup: Popup {
                            y: comboBox.height
                            width: comboBox.width
                            implicitHeight: contentItem.implicitHeight
                            padding: 0
                            background: Rectangle {
                                color: "white"
                                border.color: "#cccccc" // subtle gray border
                                border.width: 1
                                radius: 6
                            }

                            contentItem: ListView {
                                clip: true
                                implicitHeight: contentHeight
                                model: comboBox.delegateModel
                                currentIndex: comboBox.highlightedIndex
                                interactive: true
                                delegate: comboBox.delegate
                            }
                        }

                        // Show the flag only if a real selection is made
                        contentItem: Text {
                            anchors.centerIn: parent
                            text: comboBox.currentIndex > 0 ? comboBox.currentText : ""
                            font.pixelSize: 20
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Show the translation icon when no country is selected (default state)
                        Image {
                            id: translation
                            width: 32
                            height: 23
                            source: "images/translation.png"
                            anchors.centerIn: parent
                            fillMode: Image.PreserveAspectFit
                            visible: comboBox.currentIndex === 0
                        }

                        // Optional: Clean look for popup items
                        delegate: ItemDelegate {
                            width: comboBox.width
                            contentItem: Text {
                                text: model.text === "" ? "-" : model.text
                                font.pixelSize: 20
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }

                        // Set default index to 0
                        Component.onCompleted: comboBox.currentIndex = 0
                    }

                    Button {
                        id: locationButton
                        height: input_comp.height
                        text: qsTr("")
                        property bool isActive: false
                        width: 40
                        flat: true
                        opacity: rectangle.selectedContactId.length > 0 ? 1.0 : 0.5

                        Image {
                            id: location_icon1
                            x: -201
                            y: 62
                            width: 30
                            height: 28
                            source: "images/marker.png"
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                        }

                        Connections {
                            target: locationButton
                            function onClicked() {
                                if (rectangle.selectedContactId.length > 0) {
                                        chatBackend.shareLocation(
                                                    rectangle.selectedContactId)

                                    // Clear the message input after sending
                                    messageText.text = ""
                                } else {
                                    console.log("No contact selected")
                                }
                            }
                        }
                    }
                    Rectangle {
                        id: input_comp
                        width: 380
                        height: messageText.implicitHeight
                        color: "#eeeeee"
                        radius: 15

                        TextEdit {
                            id: messageText
                            height: messageText.implicitHeight
                            text: ""
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.leftMargin: 0
                            anchors.rightMargin: 0
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Text.Wrap
                            font.styleName: "Medium"
                            rightPadding: 50
                            leftPadding: 12
                            bottomPadding: 12
                            topPadding: 12
                            clip: false

                            Connections {
                                target: messageText
                                function onTextChanged() { chatBackend.on_text_changed() }
                            }
                        }

                        Text {
                            id: placeholder
                            text: qsTr("Send a message")
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: 12
                            font.pixelSize: 14
                            color: "#80000000"
                            // show only when the input is empty
                            visible: messageText.text.length === 0
                        }

                        Button {
                            id: sendButton
                            x: 166
                            width: 34
                            text: qsTr("")
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 9
                            anchors.topMargin: 0
                            anchors.bottomMargin: 0
                            icon.color: "#00ffffff"
                            flat: true
                            opacity: rectangle.selectedContactId.length > 0 ? 1.0 : 0.5
                            Rectangle {
                                id: rectangle3
                                color: "#00ffffff"
                                anchors.fill: parent
                                anchors.topMargin: 0
                            }

                            Image {
                                id: send
                                width: 31
                                height: 20
                                source: "images/send.png"
                                anchors.centerIn: parent
                                fillMode: Image.PreserveAspectFit
                            }

                            Connections {
                                target: sendButton
                                function onClicked() {
                                    if (messageText.text.length > 0
                                            && rectangle.selectedContactId.length > 0) {

                                    chatBackend.sendMessage(
                                        rectangle.selectedContactId,
                                        messageText.text,
                                        comboBox.currentValue)
                                    messageText.text = ""
                                    }
                                    else {
                                    console.log("Message is empty or no contact selected")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
