/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls

Rectangle {
    id: rectangle
    width: 400
    height: 230
    color: "#ffffff"
    radius: 16
    clip: true 

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.AllButtons
    }

    Column {
        id: column
        anchors.fill: parent
        spacing: 12
        padding: 14

        Row {
            id: row
            spacing: 8

            Rectangle {
                id: contact_icon
                width: 44
                height: 44
                color: "#8a54ff"
                radius: 500

                Image {
                    id: contact_icon_image
                    width: 25
                    height: 17
                    source: "../images/contact_icon.png"
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                }
            }

            Column {
                id: column1
                width: 200
                anchors.verticalCenter: parent.verticalCenter
                spacing: 2

                Text {
                    id: text1
                    text: qsTr("Search Contact")
                    font.pixelSize: 15
                    font.styleName: "Semibold"
                }

                Text {
                    id: text2
                    color: "#767676"
                    text: qsTr("Search users you want to chat with")
                    font.pixelSize: 14
                }
            }
        }

        Rectangle {
            id: userIdBg
            height: userIdInput.implicitHeight
            color: "#eeeeee"
            radius: 16
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 14
            anchors.rightMargin: 14
            clip: true

            TextInput {
                id: userIdInput
                text: ""
                anchors.fill: parent
                font.pixelSize: 14
                verticalAlignment: Text.AlignVCenter
                font.styleName: "Medium"
                topPadding: 12
                padding: 10
                bottomPadding: 12
            }

    Text {
        id: userIdPlaceholder
        text: qsTr("User ID")
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10
        font.pixelSize: 14
        color: "#80000000"
        // show only when the input is empty
        visible: userIdInput.text.length === 0
        MouseArea { anchors.fill: parent; onClicked: userIdInput.forceActiveFocus() }
    }
        }

        Rectangle {
            id: server_id_input
            height: serverIdInput.implicitHeight
            color: "#eeeeee"
            radius: 16
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 14
            anchors.rightMargin: 14
            clip: true
            TextInput {
                id: serverIdInput
                text: ""
                anchors.fill: parent
                font.pixelSize: 14
                verticalAlignment: Text.AlignVCenter
                font.styleName: "Medium"
                topPadding: 12
                padding: 10
                bottomPadding: 12
            }
                Text {
                    id: serverIdPlaceholder
                    text: qsTr("Server ID")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    font.pixelSize: 14
                    color: "#80000000"
                    // show only when the input is empty
                    visible: serverIdInput.text.length === 0
                    MouseArea { anchors.fill: parent; onClicked: serverIdInput.forceActiveFocus() }
                }
            
        }

        Button {
            id: add_contact_button
            height: 43
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 14
            anchors.rightMargin: 14
            flat: true

            Rectangle {
                id: rectangle1
                color: "#1f5cf1"
                radius: 16
                anchors.fill: parent

                Text {
                    id: text3
                    color: "#ffffff"
                    text: qsTr("Start Chat")
                    font.pixelSize: 14
                    font.styleName: "Semibold"
                    anchors.centerIn: parent
                }
            }

            Connections {
                target: add_contact_button
                function onClicked() { if (userIdInput.text.length > 0 && serverIdInput.text.length > 0) {
        chatBackend.addContact(
                    userIdInput.text.replace("@", ""), serverIdInput.text.replace("@", ""))
    }else {
                                        console.log("Empty userId or serverId, cannot add contact")
                                    } }
            }
        }
    }
    states: [
        State {
            name: "clicked"
        }
    ]
}
