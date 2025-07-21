import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    anchors.fill: parent
    color: "#80000000"
    visible: visible

    signal dismissed()

    MouseArea {
        anchors.fill: parent
        onClicked: dismissed()
    }

    Loader {
        source: "AddContact.qml"
        anchors.centerIn: parent
    }
}
