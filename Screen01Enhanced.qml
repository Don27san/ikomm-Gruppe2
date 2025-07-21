import QtQuick
import QtQuick.Controls
import UntitledProject4
import QtQuick.Studio.DesignEffects
import QtQuick.Layouts

Rectangle {
    id: rectangle
    width: 500
    height: 700
    color: "#ffffff"
    
    ColumnLayout {
        anchors.fill: parent
        spacing: 0

    // Chat messages area

    ListView {
    id: chatListView
    Layout.fillWidth: true
    Layout.fillHeight: true
    model: chatModel
    delegate: MessageDelegate { … }
    clip: true
    spacing: 4
    padding: 8

    // When you get new messages:
    onCountChanged: positionViewAtEnd()
}
    ListView {
        id: chatListView
        model: ListModel {
            id: chatModel
        }
        
        delegate: Rectangle {
            width: chatListView.width
            height: messageText.implicitHeight + 20
            color: "#f0f0f0"
            radius: 10
            
            Text {
                id: messageText
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                anchors.margins: 10
                text: model.author + ": " + model.message
                wrapMode: Text.Wrap
                font.pixelSize: 14
            }
        }
    }
    
    // Connections to backend
    Connections {
        target: chatBackend
        function onMessageReceived(message, author, timestamp) {
            chatModel.append({
                "message": message,
                "author": author,
                "timestamp": timestamp
            })
            chatListView.positionViewAtEnd()
        }
    }

    Rectangle {
        id: rectangle2
        Layout.fillWidth: true
        Layout.preferredHeight: input_comp.implicitHeight + 24
        color: "#ffffff"

        RowLayout {
            id: row
            Layout.fillWidth: true
            Layout.preferredHeight: input_comp.implicitHeight + 24
            spacing: 10

            RowLayout {
                id: row1
                Layout.preferredWidth: 120
                Layout.fillHeight: true

                Button {
                    id: location_button
                    Layout.preferredWidth: 55
                    Layout.preferredHeight: 52
                    text: qsTr("")
                    anchors.verticalCenter: parent.verticalCenter
                    flat: true

                    Rectangle {
                        id: rectangle1
                        color: "#ffffff"
                        anchors.fill: parent
                    }

                    Image {
                        id: location_icon   
                        width: 30
                        height: 28
                        source: "images/marker.png"
                        anchors.centerIn: parent
                        fillMode: Image.PreserveAspectFit
                    }
                }

                Button {
                    id: translation_button
                    Layout.preferredWidth: 55
                    Layout.preferredHeight: 52
                    text: qsTr("")
                    anchors.verticalCenter: parent.verticalCenter
                    property bool isActive: false
                    flat: true
                    Rectangle {
                        id: rectangle4
                        color: "#ffffff"
                        anchors.fill: parent
                    }

                    Image {
                        id: translation
                        width: 32
                        height: 23
                        source: "images/translation.png"
                        anchors.centerIn: parent
                        fillMode: Image.PreserveAspectFit
                    }

                    Connections {
                        target: translation_button
                        function onClicked() { row2.is_visible = true }
                    }
                }
            }

            Rectangle {
                id: input_comp
                Layout.fillWidth: true
                Layout.preferredHeight: textEdit.implicitHeight + 24
                color: "#eeeeee"
                radius: 15
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 10

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 8

                    TextEdit {
                        id: textEdit
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: qsTr("Send a message")
                        font.pixelSize: 14
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.Wrap
                        font.styleName: "Medium"
                        rightPadding: 40
                        leftPadding: 12
                        bottomPadding: 12
                        topPadding: 12
                        clip: false
                        Keys.onReturnPressed: {
                            if (textEdit.text.trim() !== "Send a message" && textEdit.text.trim() !== "") {
                                chatBackend.sendMessage(textEdit.text.trim())
                                textEdit.text = "Send a message"
                            }
                        }
                    }

                    Button {
                        id: send_button
                        implicitWidth: 40
                        implicitHeight: 40
                        flat: true
                        onClicked: {
                            if (textEdit.text.trim() !== "Send a message" && textEdit.text.trim() !== "") {
                                chatBackend.sendMessage(textEdit.text.trim())
                                textEdit.text = "Send a message"
                            }
                        }

                        Rectangle {
                            id: rectangle3
                            color: "#00ffffff"
                            anchors.fill: parent
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
    
    Frame {
        id: frame
        Layout.preferredHeight: 66
        Layout.fillWidth: true
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0

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
            text: qsTr("Gruppenchat IK 2025")
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

    Row {
        id: row2
        x: 150
        y: 150
        width: 123
        height: 50
        visible: row2.is_visible
        property bool is_visible: false
        padding: 8
        topPadding: 8
        spacing: 10

        Image {
            id: german
            width: 24
            height: 24
            anchors.verticalCenter: parent.verticalCenter
            source: "images/german.png"
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: text2
            text: qsTr("German")
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: 16
            font.styleName: "Medium"
        }

        Connections {
            target: row2
            function onActiveFocusChanged() { console.log("clicked") }
        }
    }
    }
}
