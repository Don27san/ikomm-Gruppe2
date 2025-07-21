import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: inputBar
    height: inputField.implicitHeight + 24
    color: "#ffffff"
    property var backend
    signal sendMessage(string text)
    signal requestLocation()

    RowLayout {
        anchors.fill: parent; spacing: 4; Layout.margins: 10

        ComboBox {
            id: comboBox; width: 50; height: inputField.implicitHeight + 24
            model: ListModel {
                ListElement { text: "" }    // shows translation icon
                ListElement { text: "🇩🇪" }
                ListElement { text: "🇨🇳" }
                ListElement { text: "🇬🇧" }
                ListElement { text: "🇹🇷" }
            }
//            indicator: Item{}; clip: true
            contentItem: Text {
                anchors.centerIn: parent
                text: comboBox.currentIndex > 0 ? comboBox.currentText : ""
                font.pixelSize: 20
            }
            Image {
                source: "images/translation.png"
                width: 32; height: 23; anchors.centerIn: parent
                visible: comboBox.currentIndex === 0
            }
            onActivated: comboBox.focus = false
            Component.onCompleted: comboBox.currentIndex = 0
        }

        Button {
            id: locBtn; width: 40; flat: true
            contentItem: Image {
                source: "images/marker.png"
                width: 30; height: 28; anchors.centerIn: parent
            }
            onClicked: requestLocation()
        }

        Rectangle {
            id: inputComp
            Layout.fillWidth: true
            height: inputField.implicitHeight + 24
            color: "#eeeeee"; radius: 15

            TextEdit {
                id: inputField
                anchors.fill: parent; anchors.margins: 12
                wrapMode: Text.Wrap; font.pixelSize: 14
                placeholderText: qsTr("Send a message")
                verticalAlignment: Text.AlignVCenter
                Keys.onReturnPressed: sendMessage(inputField.text)
            }

            Button {
                id: sendBtn; width: 34; height: inputField.implicitHeight + 24; flat: true
                anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
                contentItem: Image {
                    source: "images/send.png"
                    width: 31; height: 20; anchors.centerIn: parent
                }
                onClicked: sendMessage(inputField.text)
            }
        }
    }

    Connections {
        target: this
        onSendMessage: {
            var t = text.trim()
            if (t.length) {
                backend.sendMessage(t)
                inputField.text = ""
            }
        }
        onRequestLocation: backend.sendLocation()
    }
}
