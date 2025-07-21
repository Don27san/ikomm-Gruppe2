

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject4
import QtQuick.Studio.DesignEffects
import QtQuick.Timeline 1.0
import "components"

Rectangle {
    id: rectangle
    width: 750
    height: 700
    color: "#ffffff"
    property string selectedContactId: ""

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

    property bool showAddContact: false

    ListModel {
        id: contactsModel

        ListElement {
            contactId: "user1@server1"
            userId: "user1"
            serverName: "server1"
            userInitials: "U1"
            avatarColor: "#afdeff"
        }

        ListElement {
            contactId: "user2@server2"
            userId: "user2"
            serverName: "server2"
            userInitials: "U2"
            avatarColor: "#ffafaf"
        }
    }

    ListModel {
        id: chatModel

        // Example entries with flattened properties:
        ListElement {
            isOwn: false
            userInitials: "U2"
            avatarColor: "#ffafaf"
            messageType: "location"
            messageText: ""
            userId: "User2"
            isGroupedMessage: true
        }

        ListElement {
            isOwn: false
            userInitials: "U2"
            avatarColor: "#ffafaf"
            messageType: "text"
            messageText: "Hello there!"
            userId: ""
            isGroupedMessage: false
        }

        ListElement {
            isOwn: true
            userInitials: "U1"
            avatarColor: "#afdeff"
            messageType: "text"
            messageText: "Hi! How are you?"
            userId: ""
            isGroupedMessage: false
        }

        ListElement {
            isOwn: false
            userInitials: "U2"
            avatarColor: "#ffafaf"
            messageType: "typing"
            messageText: "Hello there!"
            userId: ""
            isGroupedMessage: false
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
                    userId: model.userId
                    serverName: model.serverName
                    userInitials: model.userInitials
                    avatarColor: model.avatarColor

                    //onContactClicked: function(clickedContactId) {
                    //   selectContact(clickedContactId)
                    // }
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
                            rectangle.selectedContactId = contactsListView.currentItem.contactId
                            chatBackend.contactClicked(
                                        rectangle.selectedContactId)
                        }
                    }
                }

                Connections {
                    target: chatBackend
                    function onContactAdded(contactId, userId, serverId, userInitials, avatarColor) {
                        console.log("Adding contact:", contactId)
                        contactsModel.append({
                            contactId: contactId,
                            userId: userId,
                            serverName: serverId,
                            userInitials: userInitials,
                            avatarColor: avatarColor
                        })
                    }
                }

                // Selection behavior
                //onCurrentIndexChanged: {
                //    if (currentIndex >= 0) {
                //        selectContactByIndex(currentIndex)
                //    }
                // }
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

                Image {
                    id: group
                    width: 37
                    height: 37
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    source: "images/group.png"
                    fillMode: Image.PreserveAspectFit
                }

                Text {
                    id: text1
                    x: 51
                    y: 11
                    text: qsTr("Chat with <UserId>")
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

            ListView {
                id: chatListView
                anchors.fill: parent
                anchors.topMargin: 66
                anchors.bottomMargin: chat_controls.height
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                clip: true

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
                        indicator: Item {}

                        model: ListModel {
                            ListElement {
                                text: ""
                            } // ⬅️ Default item, triggers icon
                            ListElement {
                                text: "🇩🇪"
                            }
                            ListElement {
                                text: "🇨🇳"
                            }
                            ListElement {
                                text: "🇬🇧"
                            }
                            ListElement {
                                text: "🇹🇷"
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
                        id: location
                        height: input_comp.height
                        text: qsTr("")
                        property bool isActive: false
                        width: 40
                        flat: true
                        Rectangle {
                            id: rectangle7
                            color: "#ffffff"
                        }

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
                            //MouseArea { anchors.fill: parent; onClicked: messageText.forceActiveFocus() }
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
                                        // Parse the contactId to get userId and serverId
                                        var parts = rectangle.selectedContactId.split(
                                                    "@")
                                        if (parts.length === 2) {
                                            var userId = parts[0]
                                            var serverId = parts[1]

                                            // Call the Python backend function
                                            chatBackend.sendMessage(
                                                        userId, serverId,
                                                        messageText.text)

                                            // Clear the message input after sending
                                            messageText.text = ""
                                        } else {
                                            console.log("Invalid contact ID format:",
                                                        rectangle.selectedContactId)
                                        }
                                    } else {
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
