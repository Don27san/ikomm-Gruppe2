
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/`qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import UntitledProject4
import QtQuick.Studio.DesignEffects
import QtQuick.Layouts

Rectangle {
    // Overlay for AddContact popup


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
        id: chatModel
    }
    id: rectangle
    width: 500
    height: 700
    visible: true
    color: "#ffffff"

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        layer.enabled: false
        layer.format: ShaderEffectSource.Alpha

        RowLayout {
            id: chatTopRow
            Layout.margins: 10
            Layout.preferredHeight: 66
            Layout.fillWidth: true
            visible: true
            spacing: 0
            Layout.minimumHeight: 0
            clip: false

            Image {
                id: group
                Layout.preferredWidth: 37
                Layout.preferredHeight: 37
                Layout.alignment: Qt.AlignVCenter
                Layout.leftMargin: 0
                source: "images/group.png"
                fillMode: Image.PreserveAspectFit
            }

            Text {
                id: text1
                text: qsTr("Gruppenchat IK 2025")
                font.pixelSize: 16
                font.styleName: "Semibold"
                Layout.alignment: Qt.AlignVCenter
                // Optionally add left margin if needed for spacing
                Layout.leftMargin: 14
            }

            Item { Layout.fillWidth: true }

            Image {
                id: tum
                Layout.preferredWidth: 49
                Layout.preferredHeight: 23
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight
                Layout.rightMargin: 0
                source: "images/tum.png"
                fillMode: Image.PreserveAspectFit
            }
        }

        ListView {
            id: chatListView
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 16
            model: chatModel
            clip: true
            spacing: 4
ScrollBar.vertical: ScrollBar {
  policy: ScrollBar.Auto
  width: 8
}

            delegate: MessageDelegate {
                message: model.message
                outgoing: false
            }
        }

        // Use ChatConnections component for backend message handling
        Loader {
            source: "components/ChatConnections.qml"
            active: true
            onLoaded: {
                item.chatModel = chatModel;
                item.chatListView = chatListView;
                item.chatBackend = chatBackend;
            }
        
        }

        RowLayout {
            id: chatBottomRow
            Layout.margins: 10
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            spacing: 0

            RowLayout {
                id: chatFunctionsRow

                Button {
                    id: location_button
                    text: ""
                    flat: true
                    Layout.preferredWidth: 50
                    Layout.preferredHeight: 50

                    icon.source: "images/marker.png"
                    icon.width: parent.height
                    icon.height: parent.width
                    icon.color: undefined

                    onClicked: showAddContact = true
                }

                Button {
                    id: translation_button
                    text: ""
                    flat: true
                    Layout.preferredWidth: 50
                    Layout.preferredHeight: 50

                    icon.source: "images/translation.png"
                    icon.width: parent.height
                    icon.height: parent.width
                    icon.color: undefined

                    //onClicked: chatBackend.sendMessage("location")
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Rectangle {
                id: input_comp
                Layout.preferredWidth: 350
                color: "#eeeeee"
                radius: 15
                Layout.preferredHeight: 50
                Layout.fillHeight: false
                Layout.rightMargin: 0
                Layout.bottomMargin: 0

                TextField {
                    id: textField
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.right: send_button.left
                    anchors.rightMargin: 8
                    placeholderText: qsTr("Send a message")
                    background: null
                    padding: 12

                    Keys.onReturnPressed: {
                        if (textField.text.trim() !== "" && textField.text.trim() !== qsTr("Send a message")) {
                            chatBackend.sendMessage(textField.text.trim())
                            textField.text = ""
                        }
                    }
                }

                Button {
                    id: send_button
                    text: ""
                    flat: true
                    width: 50
                    height: 50
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.rightMargin: 8
                    icon.source: "images/send.png"
                    icon.width: parent.height
                    icon.height: parent.width
                    icon.color: undefined

                    onClicked: {
                        if (textField.text.trim() !== "" && textField.text.trim() !== qsTr("Send a message")) {
                            chatBackend.sendMessage(textField.text.trim())
                            textField.text = ""
                        }
                    }
                }
            }
        }
    }
}
