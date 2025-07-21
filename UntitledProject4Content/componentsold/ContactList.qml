import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    signal contactSelected(string contactId)
    color: "#ffffff"; border.color: "#d0d3d7"; border.width: 1

    ListModel { id: contactModel /* populated by backend */ }

    ListView {
        anchors.fill: parent
        model: contactModel
        delegate: ContactDelegate {
            userId: model.userId
            serverId: model.serverId
            profilePicture: model.profilePicture
            onClicked: contactSelected(model.userId)
        }
    }
}