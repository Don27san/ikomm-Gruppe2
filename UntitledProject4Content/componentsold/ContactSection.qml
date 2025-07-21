import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: contactSection
    width: 250; color: "#ffffff"; border.color: "#d0d3d7"
    signal contactSelected(string userId)
    signal addContactRequested()

    ListModel { id: contactModel }
    // …populate contactModel { userId, serverId, profilePicture? } in your logic…

    ColumnLayout {
        anchors.fill: parent; spacing: 0

        Frame {
            id: header; Layout.fillWidth: true; height: 66
            RowLayout {
                anchors.fill: parent; Layout.margins: 0; spacing: 0
                Text {
                    text: qsTr("My Contacts")
                    font.pixelSize: 16; font.styleName: "Semibold"
                    anchors.verticalCenter: parent.verticalCenter
                }
                Item { Layout.fillWidth: true }
                Button {
                    id: addBtn; flat: true; width: 55; height: 52
                    anchors.verticalCenter: parent.verticalCenter
                    contentItem: Image {
                        source: "images/new_contact.png"
                        width: 20; height: 20; anchors.centerIn: parent
                    }
                    onClicked: addContactRequested()
                }
            }
        }

        ListView {
            id: contactsList
            Layout.fillWidth: true; Layout.fillHeight: true
            model: contactModel; spacing: 0; clip: true
            delegate: ContactDelegate {
                userId: model.userId
                serverId: model.serverId
                onClicked: contactSelected(model.userId)
            }
        }
    }
}
