

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
        anchors.centerIn: parent      // center in the window
        z: 1001                       // above the overlay
        visible: showAddContact
    }

    property bool showAddContact: false

    ListModel {
        id: contactsModel
        
        ListElement {
            contactId: "user1@server1"
            userId: "user1"
            serverName: "server1"
            UserInitials: "U1"
            avataarColor: "#afdeff"
        }

        ListElement {
            contactId: "user2@server2"
            userId: "user2"
            serverName: "server2"
            UserInitials: "U2"
            avataarColor: "#ffafaf"
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
        isGroupedMessage: false
    }
    
    ListElement {
        isOwn: false
        userInitials: "U2" 
        avatarColor: "#ffafaf"
        messageType: "text"
        messageText: "Hello there!"
        userId: ""
        isGroupedMessage: true
    }
    
    ListElement {
        isOwn: true
        userInitials: "U1"
        avatarColor: "#afdeff"
        messageType: "text"
        messageText: "Hi! How are you?"
        userId: ""
        isGroupedMessage: true
    }

    ListElement {
        isOwn: false
        userInitials: "U2" 
        avatarColor: "#ffafaf"
        messageType: "typing"
        messageText: "Hello there!"
        userId: ""
        isGroupedMessage: true
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

            Column {
                id: contact_container
                anchors.fill: parent
                anchors.topMargin: 66

                Button {
                    id: contact
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row6
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon
                            width: 34
                            height: 34
                            color: "#afdeff"
                            radius: 500
                            Text {
                                id: user_name_abbreviated
                                color: "#9c000000"
                                text: qsTr("U1")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text4
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
                    }

                    Connections {
                        target: contact
                        function onClicked() {
                            console.log("Open Chat with User <UserId>")
                        }
                    }
                }

                Button {
                    id: contact1
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row7
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon1
                            width: 34
                            height: 34
                            color: "#ffafaf"
                            radius: 500
                            anchors.verticalCenter: parent.verticalCenter
                            Text {
                                id: user_name_abbreviated1
                                color: "#9c000000"
                                text: qsTr("U2")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text5
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
                    }
                }

                Button {
                    id: contact2
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row8
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon2
                            width: 34
                            height: 34
                            color: "#afffc3"
                            radius: 500
                            Text {
                                id: user_name_abbreviated2
                                color: "#9c000000"
                                text: qsTr("U3")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text6
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
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

            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.topMargin: 66
                anchors.bottomMargin: chat_controls.height
                rightPadding: 10
                leftPadding: 10

                Column {
    id: chat_container
    anchors.left: parent.left
    anchors.right: parent.right
    spacing: 32
    
    // Messages will be added here dynamically
    Repeater {
        model: chatModel // ListModel containing your messages
        
        ChatMessage {
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
                        height: textEdit.implicitHeight
                        color: "#eeeeee"
                        radius: 15

                        TextEdit {
                            id: textEdit
                            height: textEdit.implicitHeight
                            text: qsTr("Send a message")
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

                        Button {
                            id: send_button
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
                        }
                    }
                }
            }
        }
    }
}


